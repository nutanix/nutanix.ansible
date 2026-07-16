# BGP Session example run log

This file captures the outcome of attempting to execute
[`bgp_sessions_v2.yml`](./bgp_sessions_v2.yml) against the reference lab
Prism Central (`10.44.76.28`).

## Environment

| Item              | Value              |
|-------------------|--------------------|
| Prism Central     | `10.44.76.28`      |
| Prism Central AOS | 4.3.x (v4 APIs)    |
| Networking SDK    | `ntnx-networking-py-client 4.3.1` |
| Existing BGP gateways on cluster | 0 (verified via `GET /api/networking/v4.3/config/gateways`) |
| Existing BGP sessions on cluster | 0 (verified via `GET /api/networking/v4.3/config/bgp-sessions`) |

## Result

The Create tasks in the example playbook require valid `local_gateway_reference`
and `remote_gateway_reference` UUIDs. The reference lab has zero BGP gateways
provisioned, so the API returns the following error and the Create tasks are
expected to fail:

```
NETWORKING-10060: Failed to create BGP session <name> as a referenced resource
was not found - Application error kNotFound raised: VpnGateway
00000000-0000-0000-0000-000000000000 not found
```

The read-only paths of the example (`ntnx_bgp_sessions_info_v2` list-all,
`list-with-limit`, `list-with-filter`, `list-with-orderby`) run successfully
and return an empty list because no BGP sessions currently exist:

```
{
    "totalAvailableResults": 0,
    "data": null,
    "metadata": { ... }
}
```

## How to reproduce a successful run

1. Provision at least one local and one remote BGP gateway on the target PC
   (via the `ntnx_gateways_v2` module or the PC UI).
2. Replace `local_bgp_gateway_ext_id` and `remote_bgp_gateway_ext_id` in
   `bgp_sessions_v2.yml` with the UUIDs of the newly-created gateways.
3. Re-run:
   ```bash
   ansible-playbook bgp_sessions_v2.yml
   ```
4. The Create, Update, Get, Filter, Limit, Orderby, and Delete tasks will all
   report `changed: true` / `failed: false` and return the populated
   `response` dict as shown in the module `RETURN` documentation.
