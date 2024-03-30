from woocommerce import API
import requests
from datetime import date

def ejecutar_script():
    wcapi = API(
        url="https://2d.com.co",
        consumer_key="ck_71bde58c9c399a383de844454801252067515028",
        consumer_secret="cs_59b05e7b0e065e72676dbab68765b375d81d15fb",
        version="wc/v3"
    )

    try:
        response = wcapi.get("orders", params={"per_page": 1, "order": "desc", "orderby": "date"})
        response.raise_for_status()
        orders = response.json()

        if orders:
            last_order = orders[0]
            ecommerce_client_id = last_order.get('customer_id')
            billing_info = last_order.get('billing')
            
            ecommerce_client_first_name = billing_info['first_name']
            ecommerce_client_last_name = billing_info['last_name']
            ecommerce_client_email = billing_info['email']
            ecommerce_client_phone = billing_info.get('phone', 'No especificado')
            ecommerce_client_gender = "No especificado"

            print("Datos del cliente de WooCommerce:")
            print(f"ID del cliente: {ecommerce_client_id}")
            print(f"Nombre del cliente: {ecommerce_client_first_name}")
            print(f"Apellido del cliente: {ecommerce_client_last_name}")
            print(f"Correo electrónico: {ecommerce_client_email}")
            print(f"Teléfono: {ecommerce_client_phone}")
            print(f"Género: {ecommerce_client_gender}")
            
            today = date.today()
            fechaActual = today.strftime("%d-%b-%Y")

            client_id = "1000.321C6YP3RBKVRBSLAV98PQW4586NMP"
            client_secret = "1eab97c69d5a7ed37d739707d611ee52504e0100fe"
            api_url = f"https://accounts.zoho.com/oauth/v2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials&scope=ZohoCreator.form.CREATE,ZohoCreator.report.READ&soid=ZohoCreator.796008741"
            response = requests.post(api_url)

            quantity = 1
            unitPrice = 80000
            totalOrder = quantity * unitPrice
            totalPayment = quantity * unitPrice

            auth = response.json().get("access_token")
            header = {"Authorization": "Zoho-oauthtoken " + auth}

            clientJSON = {
                "dni": ecommerce_client_id,
                "fname": ecommerce_client_first_name,
                "lname": ecommerce_client_last_name,
                "gender": ecommerce_client_gender,
                "email": ecommerce_client_email,
                "phone": ecommerce_client_phone,
            }

            fetch_url = "https://www.zohoapis.com/creator/custom/bilabmaster/moc_client?publickey=PCF7HeAXEHk8w5Gxu2qJpEheO"
            response3 = requests.post(fetch_url, json=clientJSON)
            clientID = str(response3.json().get("result"))

            ticket_url = "https://creator.zoho.com/api/v2.1/bilabmaster/2d-app/report/adminBoleteriaReport?nombreBoleteria=Earlytime"
            response4 = requests.get(ticket_url, headers=header)
            ticketID = response4.json().get("data")[0].get("ID")
            precioUnit = response4.json().get("data")[0].get("precioUnitBoleta")
            eventID = response4.json().get("data")[0].get("relatedEvento").get("ID")

            catCont_url = "https://creator.zoho.com/api/v2.1/bilabmaster/2d-app/report/categoriasContablesReport?nombreCategoria=Ventas"
            response5 = requests.get(catCont_url, headers=header)
            catID = response5.json().get("data")[0].get("ID")

            orderJSON = {
                "data": {
                    "relatedEvento": eventID,
                    "origenOrden": "Preventa",
                    "Vendedor": "ECommerce",
                    "fechaVenta": fechaActual, 
                    "idOrden": "ORD-",
                    "relatedClientes": [clientID],
                    "relatedTipoBoleta": ticketID,
                    "Cantidad": quantity,
                    "precioUnitario": precioUnit,
                    "totalOrden": totalOrder,
                    "Abonos": totalPayment,
                    "condicionPago": "Pago Total",
                    "conceptoTransaccion": "Venta",
                    "relatedPagos": [
                        {
                            "ingresoPorVenta": "true",
                            "relatedEvento": eventID,
                            "fechaTransaccion": fechaActual,
                            "tipoTransaccion": "Ingreso",
                            "relatedCategoriaContable": catID,
                            "tipoPago": "Transferencia/Datafono",
                            "pagoEfectivo": 0,
                            "pagoTransfDatafono": totalPayment,
                            "Banco": "Mercado Pago",
                            "totalTransaccion": totalPayment
                        }
                    ]
                }
            }

            order_url = "https://creator.zoho.com/api/v2.1/bilabmaster/2d-app/form/Ventas_Boleteria"
            response6 = requests.post(order_url, headers=header, json=orderJSON)
            print(response6.json())
            orderID = response6.json().get("data").get("ID")
            print("Client ID:", clientID)
            print("Order ID:", orderID)
        else:
            print("No se encontraron órdenes.")
    except Exception as e:
        print(f"Se produjo un error al obtener las órdenes: {e}")

ejecutar_script()
