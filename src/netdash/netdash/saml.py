import saml2


def create_saml_config(entity_id, sp_name, acs_post, ls_redirect, ls_post, required_attributes,
                       optional_attributes, sp_cert_file, sp_key_file, idp_metadata_file, debug=False):
    return {
        'xmlsec_binary': '/usr/bin/xmlsec1',
        # 'entityid': '%smetadata/' % SAML2_URL_BASE,
        'entityid': entity_id,  # e.g. https://yourdomain.cm/saml/metadata,

        # directory with attribute mapping
        # 'attribute_map_dir': path.join(BASEDIR, 'attribute-maps'),
        'name': sp_name,

        # this block states what services we provide
        'service': {
            'sp': {
                'name': sp_name,
                'name_id_format': ('urn:oasis:names:tc:SAML:2.0:nameid-format:transient'),
                'authn_requests_signed': 'true',
                'allow_unsolicited': True,
                'endpoints': {
                    # url and binding to the assetion consumer service view
                    # do not change the binding or service name
                    'assertion_consumer_service': [
                        (acs_post, saml2.BINDING_HTTP_POST),
                    ],
                    # url and binding to the single logout service view
                    # do not change the binding or service name
                    'single_logout_service': [
                        (ls_redirect, saml2.BINDING_HTTP_REDIRECT),
                        (ls_post, saml2.BINDING_HTTP_POST),
                    ],
                },
                'required_attributes': required_attributes,
                'optional_attributes': optional_attributes,
            },
        },

        # where the remote metadata is stored
        'metadata': {
            'local': [idp_metadata_file.name],
        },

        # set to 1 to output debugging information
        'debug': 1 if debug else 0,

        # certificate
        'key_file': sp_key_file.name,
        'cert_file': sp_cert_file.name,
    }
