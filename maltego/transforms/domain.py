from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverEntitiesTransform, registry

@registry.register_transform(
    display_name="To Dummy Subdomains [EternalWhisper]",
    input_entity="maltego.Domain",
    output_entities=["maltego.DNSName"],
    description="Placeholder transform - EternalWhisper skeleton test"
)
class DomainToDummySubdomains(DiscoverEntitiesTransform):
    def create_entities(self, request: MaltegoMsg, response: MaltegoTransform):
        domain = request.Value
        response.addEntity("maltego.DNSName", f"test1.{domain}")
        response.addEntity("maltego.DNSName", f"test2.{domain}")
        response.addUIMessage(f"EternalWhisper placeholder executed on {domain}")
