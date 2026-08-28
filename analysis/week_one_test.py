B=100
print(f"BUDGET ${B} — what it buys\n")
print("Signings (the thing you'd call traction):")
for cac in (240,400,600,800):
    print(f"  CAC ${cac:>3}: expected {B/cac:>4.2f} signings  -> P(zero) is the overwhelming case")
print("\nQuiz completions (the readable signal):")
for cpq in (3,5,10,20,40):
    print(f"  ${cpq:>2}/quiz: {B/cpq:>5.1f} completions")
print("\nWhat cost-per-quiz has to be, to back into a viable CAC:")
print("  (CAC = cost_per_quiz / quiz-to-signed rate)")
for rate in (0.02,0.03,0.05):
    print(f"  at {rate*100:>2.0f}% quiz->signed: ${400*rate:>5.2f}/quiz = $400 CAC ; ${800*rate:>5.2f}/quiz = $800 CAC")
print("\nMeta learning phase needs ~50 conversions/ad set to exit.")
for cpq in (3,5,10):
    print(f"  at ${cpq}/quiz, ${B} = {B/cpq:.0f} conversions = {B/cpq/50*100:.0f}% of the way out of learning")
print("\nPacing: same $100, different concentration")
for d,day in ((7,100/7),(4,25.0),(3,100/3)):
    print(f"  {d} days at ${day:>5.2f}/day")
