def reconcile(invoices, payments):
    results = []

    for inv in invoices:
        match = next(
            (
                p for p in payments
                if p.vendor == inv.vendor
                and abs(p.paid_amount - inv.amount) <= 1
            ),
            None
        )

        if match:
            inv.status = "MATCHED"
            results.append((inv.id, match.id, "MATCHED"))
        else:
            inv.status = "UNMATCHED"
            results.append((inv.id, None, "UNMATCHED"))

    return results
