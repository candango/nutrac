#!/usr/bin/env python
#
# Copyright 2018 Flavio Garcia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# TODO: Private key methods belong to podship_platform project
def generate_private_key():
    """ FROM pyraspora: pyaspora.user.models
    Generate a 4096-bit RSA key. The key will be stored in the User
    object. The private key will be protected with password <passphrase>,
    which is usually the user password.
    """
    # TODO: seems to be candidate as part of some security toolkit
    from Crypto.PublicKey import RSA
    RSAkey = RSA.generate(4096)
    return RSAkey.exportKey(
        format='PEM',
        pkcs=1
    ).decode("ascii")
