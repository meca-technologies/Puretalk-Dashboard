import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'ACa6902364cdd0dd9f9b4ea4a86498f71a'
auth_token = 'efa74a9aa01c33e162fc793aa5d46a30'
client = Client(account_sid, auth_token)



#customer_profiles_channel_endpoint_assignment = client.trusthub \
#    .customer_profiles('BU7881987e305f5adaa84722530d01ab53') \
#    .customer_profiles_channel_endpoint_assignment \
#    .create(
#         channel_endpoint_type='phone-number',
#         channel_endpoint_sid='PN9058a85e469915cf60ff64e5f6512fa7'
#     )
#
#trust_products_channel_endpoint_assignment = client.trusthub \
#    .trust_products('BUbe02d7b7a1a55491f0941cd68e4d422d') \
#    .trust_products_channel_endpoint_assignment \
#    .create(
#         channel_endpoint_type='phone-number',
#         channel_endpoint_sid='PN9058a85e469915cf60ff64e5f6512fa7'
#     )
#
#trust_products = client.trusthub \
#                .trust_products('BUbe02d7b7a1a55491f0941cd68e4d422d') \
#                .update(status='pending-review')

customer_profiles_channel_endpoint_assignment = client.trusthub \
    .trust_products('BUbe02d7b7a1a55491f0941cd68e4d422d') \
    .trust_products_channel_endpoint_assignment \
    .list(limit=20)

for record in customer_profiles_channel_endpoint_assignment:
    print(record.__dict__)