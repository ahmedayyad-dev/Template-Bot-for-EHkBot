# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.

from importlib.util import module_from_spec, spec_from_file_location

spec = spec_from_file_location("info", "../../../info.py")
info = module_from_spec(spec)
spec.loader.exec_module(info)
FBotToken = info.FBotToken
Fowner_id = info.owner_id
rapidapi_key = info.rapidapi_key
LICENSE_KEY = info.LICENSE_KEY
channel = info.channel
api_id = info.api_id
api_hash = info.api_hash
