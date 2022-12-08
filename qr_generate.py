import qrcode
import image

def create_conf(public_key, ip, client_private_key, end_point, dns, MTU, comment):
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
    QR = qrcode.make(template)
    QR.save("QR.png")
    file = open(f"configs/{comment}.conf", "w")
    file.write(template)
    file.close()
    return template
def show(comment):
    config = open(f"configs/{comment}.conf", "r")
    QR = qrcode.make(config.read())
    config.close()
    QR.save("QR.png")