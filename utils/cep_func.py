from brazilcep import get_address_from_cep, WebService

def get_address_by_cep(cep: str) -> dict:
    try:
        address = get_address_from_cep(cep, webservice=WebService.CORREIOS)

        return address

    except Exception as e:
        print(f"Error: {e}")

