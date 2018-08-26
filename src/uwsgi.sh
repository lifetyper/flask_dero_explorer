#!/bin/bash
uwsgi -s /tmp/dexp.sock --manage-script-name --mount /dexp=manage:app --process 5