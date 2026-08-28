def sim(new_per_mo, price=200, start_mrr=745, median_life=5.9, months=12, cap=20, start_n=6):
    churn = 1 - 0.5**(1/median_life)
    mrr, n, total = start_mrr, start_n, 0.0
    for _ in range(months):
        mrr *= (1-churn); n *= (1-churn)
        add = min(new_per_mo, max(0, cap-n))
        mrr += add*price; n += add
        total += mrr
    return total, mrr, n

print(f"{'new/mo':>7} {'12mo collected':>15} {'end MRR':>9} {'end run-rate':>13} {'athletes':>9}")
for r in [0.5,1,1.5,2,2.5,3]:
    tot,mrr,n = sim(r)
    print(f"{r:>7.1f} {'$'+format(tot,',.0f'):>15} {'$'+format(mrr,',.0f'):>9} {'$'+format(mrr*12,',.0f'):>13} {n:>9.1f}")

print("\n--- churn is the lever: 2 new/month, varying median lifetime ---")
for life in [5.9, 9, 12, 18]:
    tot,mrr,n = sim(2, median_life=life)
    ch = (1-0.5**(1/life))*100
    print(f"median {life:>4.1f}mo (churn {ch:>4.1f}%/mo): 12mo=${tot:>7,.0f}  end run-rate=${mrr*12:>7,.0f}  athletes={n:>4.1f}")

print("\n--- steady-state athletes needed for $20k/yr run-rate ---")
for price in (170,185,200):
    print(f"  at ${price}/mo: {20000/12/price:>4.1f} concurrent athletes")

print("\n--- ad budget needed at 2 new athletes/month ---")
ltv = 200*5.9
print(f"LTV at $200 x 5.9mo = ${ltv:,.0f}; at 90% margin contribution = ${ltv*0.9:,.0f}")
for cac in (240,400,600,800):
    mo = 2*cac
    print(f"  CAC ${cac:>3}: ${mo:>5,.0f}/mo (${mo/30:>5.2f}/day)  LTV:CAC = {ltv/cac:>4.1f}:1  payback {cac/(200*0.9):>3.1f} mo")
