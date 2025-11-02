import sys
import logging
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Configure logging
LOG_FILE = "/tmp/order_reminders_log.txt"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)


def main():
    # GraphQL endpoint
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=False)

    # Calculate date range
    now = datetime.now()
    week_ago = now - timedelta(days=7)
    week_ago_str = week_ago.strftime("%Y-%m-%d")
    now_str = now.strftime("%Y-%m-%d")

    # GraphQL query
    query = gql(
        """
        query GetRecentOrders($from: Date, $to: Date) {
            orders(orderDate_Gte: $from, orderDate_Lte: $to, status: "PENDING") {
                id
                customer {
                    email
                }
            }
        }
    """
    )
    variables = {"from": week_ago_str, "to": now_str}

    try:
        result = client.execute(query, variable_values=variables)
        orders = result.get("orders", [])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for order in orders:
            order_id = order["id"]
            email = order["customer"]["email"]
            logging.info(f"{timestamp} - Order ID: {order_id}, Customer Email: {email}")
        print("Order reminders processed!")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
