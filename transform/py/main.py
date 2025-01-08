# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: .venv
#     language: python
#     name: python3
# ---

# %%
import json
import duckdb

# %%
s = """
{"data":[{"stuff":[
    {"onetype":[
        {"id":1,"name":"John Doe"},
        {"id":2,"name":"Don Joeh"}
    ]},
    {"othertype":[
        {"id":2,"company":"ACME"}
    ]}]
},{"otherstuff":[
    {"thing":
        [[1,42],[2,2]]
    }]
}]}
"""

# %%
print(json.loads(s))

# %%
