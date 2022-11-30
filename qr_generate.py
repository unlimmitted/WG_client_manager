import qrcode
import image


def create_conf(public_key, ip, client_private_key, end_point, dns="1.1.1.1", MTU="1420"):
    template = f"""
    [Interface]
    PrivateKey = {client_private_key}
    Address = {ip}
    DNS = {dns}
    MTU = {MTU}
    
    [Peer]
    PublicKey = {public_key}
    AllowedIPs = 0.0.0.0/0
    Endpoint = {end_point}
    PersistentKeepalive = 30
    """
    img = qrcode.make(template)
    img.save("QR.png")
    return template

def show(public_key, ip, client_private_key, end_point, dns="1.1.1.1", MTU="1420"):
    template = f"""
        [Interface]
        PrivateKey = {client_private_key}
        Address = {ip}
        DNS = {dns}
        MTU = {MTU}

        [Peer]
        PublicKey = {public_key}
        AllowedIPs = 0.0.0.0/0
        Endpoint = {end_point}
        PersistentKeepalive = 30
        """
