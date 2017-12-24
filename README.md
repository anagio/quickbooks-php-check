# QuickBooks PHP Connection Check

## Overview

Check if your app is connected to QuickBooks with Datadog

## Installation

1. Copy the Python script for your chosen integration to the `checks.d` directory where you installed the Agent.
2. Copy the corresponding yaml configuration file to the `conf.d` directory where you installed the Agent.

## Configuration

Edit the `quickbooks_php_connected.yaml` file to point to your `diagnostics.php` URL

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        quickbooks_php_connected
        ------------------------
          - instance #0 [OK]
          - Collected 0 metrics, 0 events & 1 service check

## Compatibility

The Quickbooks PHP Connection check is compatible with https://github.com/consolibyte/quickbooks-php

