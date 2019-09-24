from django.db import models
from django.contrib.postgres.fields import ArrayField

from netfields import MACAddressField, CidrAddressField


class Admin(models.Model):
    job = models.AutoField(primary_key=True)
    entered = models.DateTimeField(blank=True, null=True)
    started = models.DateTimeField(blank=True, null=True)
    finished = models.DateTimeField(blank=True, null=True)
    device = models.GenericIPAddressField(blank=True, null=True)
    port = models.TextField(blank=True, null=True)
    action = models.TextField(blank=True, null=True)
    subaction = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    username = models.TextField(blank=True, null=True)
    userip = models.GenericIPAddressField(blank=True, null=True)
    log = models.TextField(blank=True, null=True)
    debug = models.BooleanField(blank=True, null=True)
    device_key = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin'


class Community(models.Model):
    ip = models.GenericIPAddressField(primary_key=True)
    snmp_comm_rw = models.TextField(blank=True, null=True)
    snmp_auth_tag_read = models.TextField(blank=True, null=True)
    snmp_auth_tag_write = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'community'


class DbixClassSchemaVersions(models.Model):
    version = models.CharField(primary_key=True, max_length=10)
    installed = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'dbix_class_schema_versions'


class Device(models.Model):
    ip = models.GenericIPAddressField(primary_key=True)
    creation = models.DateTimeField(blank=True, null=True)
    dns = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    uptime = models.BigIntegerField(blank=True, null=True)
    contact = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    layers = models.CharField(max_length=8, blank=True, null=True)
    ports = models.IntegerField(blank=True, null=True)
    mac = MACAddressField(blank=True, null=True)
    serial = models.TextField(blank=True, null=True)
    model = models.TextField(blank=True, null=True)
    ps1_type = models.TextField(blank=True, null=True)
    ps2_type = models.TextField(blank=True, null=True)
    ps1_status = models.TextField(blank=True, null=True)
    ps2_status = models.TextField(blank=True, null=True)
    fan = models.TextField(blank=True, null=True)
    slots = models.IntegerField(blank=True, null=True)
    vendor = models.TextField(blank=True, null=True)
    os = models.TextField(blank=True, null=True)
    os_ver = models.TextField(blank=True, null=True)
    log = models.TextField(blank=True, null=True)
    snmp_ver = models.IntegerField(blank=True, null=True)
    snmp_comm = models.TextField(blank=True, null=True)
    snmp_class = models.TextField(blank=True, null=True)
    vtp_domain = models.TextField(blank=True, null=True)
    last_discover = models.DateTimeField(blank=True, null=True)
    last_macsuck = models.DateTimeField(blank=True, null=True)
    last_arpnip = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device'


class DeviceIp(models.Model):
    ip = models.GenericIPAddressField()
    alias = models.GenericIPAddressField()
    subnet = CidrAddressField(blank=True, null=True)
    port = models.TextField(blank=True, null=True)
    dns = models.TextField(blank=True, null=True)
    creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device_ip'
        unique_together = (('ip', 'alias'),)


class DeviceModule(models.Model):
    ip = models.GenericIPAddressField()
    index = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    parent = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    # Field renamed because it was a Python reserved word.
    class_field = models.TextField(db_column='class', blank=True, null=True)
    pos = models.IntegerField(blank=True, null=True)
    hw_ver = models.TextField(blank=True, null=True)
    fw_ver = models.TextField(blank=True, null=True)
    sw_ver = models.TextField(blank=True, null=True)
    serial = models.TextField(blank=True, null=True)
    model = models.TextField(blank=True, null=True)
    fru = models.BooleanField(blank=True, null=True)
    creation = models.DateTimeField(blank=True, null=True)
    last_discover = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device_module'
        unique_together = (('ip', 'index'),)


class DevicePort(models.Model):
    ip = models.GenericIPAddressField()
    port = models.TextField()
    creation = models.DateTimeField(blank=True, null=True)
    descr = models.TextField(blank=True, null=True)
    up = models.TextField(blank=True, null=True)
    up_admin = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    duplex = models.TextField(blank=True, null=True)
    duplex_admin = models.TextField(blank=True, null=True)
    speed = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    mac = MACAddressField(blank=True, null=True)
    mtu = models.IntegerField(blank=True, null=True)
    stp = models.TextField(blank=True, null=True)
    remote_ip = models.GenericIPAddressField(blank=True, null=True)
    remote_port = models.TextField(blank=True, null=True)
    remote_type = models.TextField(blank=True, null=True)
    remote_id = models.TextField(blank=True, null=True)
    vlan = models.TextField(blank=True, null=True)
    pvid = models.IntegerField(blank=True, null=True)
    lastchange = models.BigIntegerField(blank=True, null=True)
    manual_topo = models.BooleanField()
    is_uplink = models.BooleanField(blank=True, null=True)
    slave_of = models.TextField(blank=True, null=True)
    is_master = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'device_port'
        unique_together = (('port', 'ip'),)


class DevicePortLog(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    port = models.TextField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    log = models.TextField(blank=True, null=True)
    username = models.TextField(blank=True, null=True)
    userip = models.GenericIPAddressField(blank=True, null=True)
    action = models.TextField(blank=True, null=True)
    creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device_port_log'


class DevicePortPower(models.Model):
    ip = models.GenericIPAddressField()
    port = models.TextField(primary_key=True)
    module = models.IntegerField(blank=True, null=True)
    admin = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    # Field renamed because it was a Python reserved word.
    class_field = models.TextField(db_column='class', blank=True, null=True)
    power = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device_port_power'
        unique_together = (('port', 'ip'),)


class DevicePortProperties(models.Model):
    ip = models.GenericIPAddressField()
    port = models.TextField()
    error_disable_cause = models.TextField(blank=True, null=True)
    remote_is_wap = models.BooleanField(blank=True, null=True)
    remote_is_phone = models.BooleanField(blank=True, null=True)
    remote_vendor = models.TextField(blank=True, null=True)
    remote_model = models.TextField(blank=True, null=True)
    remote_os_ver = models.TextField(blank=True, null=True)
    remote_serial = models.TextField(blank=True, null=True)
    raw_speed = models.BigIntegerField(blank=True, null=True)
    faststart = models.BooleanField(blank=True, null=True)
    ifindex = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device_port_properties'
        unique_together = (('port', 'ip'),)


class DevicePortSsid(models.Model):
    ip = models.GenericIPAddressField(primary_key=True)
    port = models.TextField()
    ssid = models.TextField(blank=True, null=True)
    broadcast = models.BooleanField(blank=True, null=True)
    bssid = MACAddressField()

    class Meta:
        managed = False
        db_table = 'device_port_ssid'
        unique_together = (('ip', 'bssid', 'port'),)


class DevicePortVlan(models.Model):
    ip = models.GenericIPAddressField()
    port = models.TextField()
    vlan = models.IntegerField()
    native = models.BooleanField()
    creation = models.DateTimeField(blank=True, null=True)
    last_discover = models.DateTimeField(blank=True, null=True)
    vlantype = models.TextField(blank=True, null=True)
    egress_tag = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'device_port_vlan'
        unique_together = (('ip', 'port', 'vlan', 'native'),)


class DevicePortWireless(models.Model):
    ip = models.GenericIPAddressField()
    port = models.TextField()
    channel = models.IntegerField(blank=True, null=True)
    power = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device_port_wireless'
        unique_together = (('ip', 'port'),)


class DevicePower(models.Model):
    ip = models.GenericIPAddressField()
    module = models.IntegerField()
    power = models.IntegerField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device_power'
        unique_together = (('ip', 'module'),)


class DeviceSkip(models.Model):
    backend = models.TextField()
    device = models.GenericIPAddressField()
    actionset = ArrayField(models.TextField(), blank=True, null=True)
    deferrals = models.IntegerField(blank=True, null=True)
    last_defer = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device_skip'
        unique_together = (('backend', 'device'),)


class DeviceVlan(models.Model):
    ip = models.GenericIPAddressField()
    vlan = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    creation = models.DateTimeField(blank=True, null=True)
    last_discover = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device_vlan'
        unique_together = (('ip', 'vlan'),)


class Hadr(models.Model):
    mac = MACAddressField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hadr'


class Log(models.Model):
    creation = models.DateTimeField(blank=True, null=True)
    # Field renamed because it was a Python reserved word.
    class_field = models.TextField(db_column='class', blank=True, null=True)
    entry = models.TextField(blank=True, null=True)
    logfile = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log'


class Macstr(models.Model):
    mac = MACAddressField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'macstr'


class NetmapPositions(models.Model):
    id = models.AutoField(primary_key=True)
    host_groups = ArrayField(models.TextField())
    vlan = models.IntegerField()
    positions = models.TextField()
    device = models.GenericIPAddressField(blank=True, null=True)
    locations = ArrayField(models.TextField())


class Node(models.Model):
    mac = MACAddressField()
    switch = models.GenericIPAddressField()
    port = models.TextField()
    vlan = models.TextField()
    active = models.BooleanField(blank=True, null=True)
    oui = models.CharField(max_length=8, blank=True, null=True)
    time_first = models.DateTimeField(blank=True, null=True)
    time_recent = models.DateTimeField(blank=True, null=True)
    time_last = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'node'
        unique_together = (('mac', 'switch', 'port', 'vlan'),)


class NodeIp(models.Model):
    mac = MACAddressField()
    ip = models.GenericIPAddressField()
    active = models.BooleanField(blank=True, null=True)
    time_first = models.DateTimeField(blank=True, null=True)
    time_last = models.DateTimeField(blank=True, null=True)
    dns = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'node_ip'
        unique_together = (('mac', 'ip'),)


class NodeMonitor(models.Model):
    mac = MACAddressField(primary_key=True)
    active = models.BooleanField(blank=True, null=True)
    why = models.TextField(blank=True, null=True)
    cc = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    matchoui = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'node_monitor'


class NodeNbt(models.Model):
    mac = MACAddressField(primary_key=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    nbname = models.TextField(blank=True, null=True)
    domain = models.TextField(blank=True, null=True)
    server = models.BooleanField(blank=True, null=True)
    nbuser = models.TextField(blank=True, null=True)
    active = models.BooleanField(blank=True, null=True)
    time_first = models.DateTimeField(blank=True, null=True)
    time_last = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'node_nbt'


class NodeWireless(models.Model):
    mac = MACAddressField(primary_key=True)
    ssid = models.TextField()
    uptime = models.IntegerField(blank=True, null=True)
    maxrate = models.IntegerField(blank=True, null=True)
    txrate = models.IntegerField(blank=True, null=True)
    sigstrength = models.IntegerField(blank=True, null=True)
    sigqual = models.IntegerField(blank=True, null=True)
    rxpkt = models.BigIntegerField(blank=True, null=True)
    txpkt = models.BigIntegerField(blank=True, null=True)
    rxbyte = models.BigIntegerField(blank=True, null=True)
    txbyte = models.BigIntegerField(blank=True, null=True)
    time_last = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'node_wireless'
        unique_together = (('mac', 'ssid'),)


class Oui(models.Model):
    oui = models.CharField(primary_key=True, max_length=8)
    company = models.TextField(blank=True, null=True)
    abbrev = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oui'


class Process(models.Model):
    controller = models.IntegerField()
    device = models.GenericIPAddressField()
    action = models.TextField()
    status = models.TextField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'process'


class Sessions(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    creation = models.DateTimeField(blank=True, null=True)
    a_session = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sessions'


class Statistics(models.Model):
    day = models.DateField(primary_key=True)
    device_count = models.IntegerField()
    device_ip_count = models.IntegerField()
    device_link_count = models.IntegerField()
    device_port_count = models.IntegerField()
    device_port_up_count = models.IntegerField()
    ip_table_count = models.IntegerField()
    ip_active_count = models.IntegerField()
    node_table_count = models.IntegerField()
    node_active_count = models.IntegerField()
    netdisco_ver = models.TextField(blank=True, null=True)
    snmpinfo_ver = models.TextField(blank=True, null=True)
    schema_ver = models.TextField(blank=True, null=True)
    perl_ver = models.TextField(blank=True, null=True)
    pg_ver = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'statistics'


class Subnets(models.Model):
    net = CidrAddressField(primary_key=True)
    creation = models.DateTimeField(blank=True, null=True)
    last_discover = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subnets'


class Topology(models.Model):
    dev1 = models.GenericIPAddressField()
    port1 = models.TextField()
    dev2 = models.GenericIPAddressField()
    port2 = models.TextField()

    class Meta:
        managed = False
        db_table = 'topology'
        unique_together = (('dev1', 'port1'), ('dev2', 'port2'),)


class UserLog(models.Model):
    entry = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    userip = models.GenericIPAddressField(blank=True, null=True)
    event = models.TextField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    creation = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_log'


class Users(models.Model):
    username = models.CharField(primary_key=True, max_length=50)
    password = models.TextField(blank=True, null=True)
    creation = models.DateTimeField(blank=True, null=True)
    last_on = models.DateTimeField(blank=True, null=True)
    port_control = models.BooleanField(blank=True, null=True)
    ldap = models.BooleanField(blank=True, null=True)
    admin = models.BooleanField(blank=True, null=True)
    fullname = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    token = models.TextField(blank=True, null=True)
    token_from = models.IntegerField(blank=True, null=True)
    radius = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
