import json
import boto3
from datetime import datetime

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """
    Lit les données JSON brutes de S3, les transforme et les écrit dans le dossier processed
    """

    # Mettez à jour le nom du bucket !
    source_bucket = 'nom-etudiant-data-lake-2024'  # VOTRE NOM DE BUCKET
    source_key = 'raw/orders_data.json'
    target_key = 'processed/orders_processed.json'

    try:
        # Lire les données brutes
        print(f"Lecture : s3://{source_bucket}/{source_key}")
        response = s3.get_object(Bucket=source_bucket, Key=source_key)
        raw_data = response['Body'].read().decode('utf-8')

        # Parser le format JSON Lines
        orders = []
        for line in raw_data.strip().split('\n'):
            if line:
                orders.append(json.loads(line))

        print(f"{len(orders)} commandes lues")

        # Opérations de transformation de données
        processed_orders = []
        total_revenue = 0

        for order in orders:
            # Calculer le prix total
            total_price = order['price'] * order['quantity']
            total_revenue += total_price

            # Données transformées
            processed_order = {
                'orderID': order['orderID'],
                'customerID': order['customerID'],
                'productName': order['productName'],
                'unitPrice': order['price'],
                'quantity': order['quantity'],
                'totalPrice': round(total_price, 2),
                'orderDate': order['orderDate'],
                'city': order['city'].upper(),  # Convertir les noms de villes en majuscules
                'country': order['country'].upper(),
                'status': order['status'],
                'processedAt': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            processed_orders.append(processed_order)

        # Statistiques
        stats = {
            'totalOrders': len(processed_orders),
            'totalRevenue': round(total_revenue, 2),
            'processedDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # Écrire les données traitées dans S3
        output_data = {
            'statistics': stats,
            'orders': processed_orders
        }

        s3.put_object(
            Bucket=source_bucket,
            Key=target_key,
            Body=json.dumps(output_data, indent=2, ensure_ascii=False),
            ContentType='application/json'
        )

        # Générer fichier JSON Lines pour S3 Select et analyse
        processed_lines = '\n'.join([json.dumps(order, ensure_ascii=False) for order in processed_orders])

        s3.put_object(
            Bucket=source_bucket,
            Key='processed/orders_lines.json',  # Nom de fichier différent
            Body=processed_lines,
            ContentType='application/json'
        )

        print(f"Données traitées écrites : s3://{source_bucket}/{target_key}")
        print(f"Statistiques : {stats}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Processus ETL réussi',
                'statistics': stats
            })
        }

    except Exception as e:
        print(f"Erreur : {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }