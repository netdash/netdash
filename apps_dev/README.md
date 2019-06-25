This directory is ignored by git, with the exception of this README, the dev-entrypoint.sh script, and the NetDash example modules.

When docker-compose is used with the included docker-compose.yml file, the dev-entrypoint.sh script will attempt to install any subdirectories in the `apps_dev` directory as Python packages in "editable" mode.

To take advantage of this in your workflow to develop NetDash apps, clone your app into the `apps_dev` directory.
