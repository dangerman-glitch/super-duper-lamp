import datetime as dt
NOW=1787961600  # 2026-08-28
# (amount_cents, start, ended_or_None)
active=[(12500,1780937098),(15000,1776886979),(7500,1773779682),
        (15000,1770329750),(12000,1735783522),(12500,1731519307)]
canceled=[(12500,1767103299,1774105673,'payment_failed'),
          (15000,1753394062,1760569078,'payment_failed'),
          (17000,1738101249,1764366849,'requested'),
          (12500,1736991826,1752630226,'requested'),
          (12500,1734490919,1782468833,'requested'),
          (13000,1726685203,1737226003,'requested'),
          (13000,1726340458,1752519658,'requested'),
          ( 7000,1723568882,1755104882,'requested'),
          (13000,1721997646,1732563958,'requested'),
          ( 7000,1718368156,1723638556,'requested'),
          (12000,1713536829,1717788108,'requested'),
          (12000,1712774672,1733258776,'requested')]
M=2629800.0  # avg month seconds
mrr=sum(a for a,_ in active)/100
print(f"ACTIVE  n={len(active)}  MRR=${mrr:,.0f}/mo  ARR=${mrr*12:,.0f}")
print(f"  price range ${min(a for a,_ in active)/100:.0f}-${max(a for a,_ in active)/100:.0f}"
      f"  mean ${mrr/len(active):.0f}  median ${sorted(a for a,_ in active)[len(active)//2]/100:.0f}")
ten=sorted((NOW-s)/M for _,s in active)
print(f"  tenure so far (mo): {[round(t,1) for t in ten]}")
print()
life=sorted((e-s)/M for _,s,e,_ in canceled)
print(f"CHURNED n={len(canceled)}  completed lifetimes (mo): {[round(x,1) for x in life]}")
print(f"  mean {sum(life)/len(life):.1f} mo   median {life[len(life)//2]:.1f} mo")
lost=sum(a for a,_,_,_ in canceled)/100
print(f"  mean churned rate ${lost/len(canceled):.0f}/mo")
pf=[x for x in canceled if x[3]=='payment_failed']
print(f"  ended by FAILED PAYMENT: {len(pf)} of {len(canceled)} ({len(pf)/len(canceled)*100:.0f}%)")
print()
avg_life=sum(life)/len(life)
avg_rate=mrr/len(active)
print(f"LTV (mean churned lifetime x mean active rate) = ${avg_life*avg_rate:,.0f}")
print(f"LTV (median lifetime {life[len(life)//2]:.1f}mo x median rate $125) = ${life[len(life)//2]*125:,.0f}")
print()
# churn rate: cancellations in trailing 12 months vs avg active base
yr=NOW-31557600
recent=[x for x in canceled if x[2]>=yr]
print(f"Cancellations in trailing 12mo: {len(recent)}")
starts=[s for _,s in active]+[s for _,s,_,_ in canceled]
print(f"New subs in trailing 12mo: {len([s for s in starts if s>=yr])}")
