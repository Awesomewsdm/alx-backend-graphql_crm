#!/bin/bash
# Script to delete inactive customers (no orders in the past year) and log the result

LOG_FILE="/tmp/customer_cleanup_log.txt"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

cd "$(dirname "$0")/../.."

DELETED_COUNT=$(python manage.py shell -c "from crm.models import Customer; from django.utils import timezone; from datetime import timedelta; one_year_ago = timezone.now() - timedelta(days=365); to_delete = Customer.objects.filter(order__isnull=True) | Customer.objects.exclude(order__created_at__gte=one_year_ago); count = to_delete.distinct().count(); to_delete.distinct().delete(); print(count)")

if [ -z "$DELETED_COUNT" ]; then
    DELETED_COUNT=0
fi

echo "$TIMESTAMP - Deleted $DELETED_COUNT inactive customers" >> "$LOG_FILE"
