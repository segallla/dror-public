// The lease, as Stage's MORE Power Fund I model sets it by default
// (leaseRentPre 0.06 $M/yr, leaseLag 2 yrs, leaseRent 0.15 $M/yr, leaseEsc 2.5%, leaseTerm 20 yrs;
// bessCap 6.5% for the value of battery rent). One pure module drives the dial, the coins and the readout.
const SRC = `
const OPTION_RENT = 60000, LEASE_RENT = 150000, ESCALATOR = 0.025, COD = 2, TERM = 20, CAP = 0.065, COIN = 250000;
// rent paid in a given (fractional) year of the lease: option rent before COD, then escalating yearly steps
function rentAt(year) {
  if (year < COD) return OPTION_RENT;
  const n = Math.min(TERM - 1, Math.floor(year - COD));
  return LEASE_RENT * Math.pow(1 + ESCALATOR, n);
}
// rent collected from year 0 up to a (fractional) year
function paidBy(year) {
  const y = Math.max(0, Math.min(COD + TERM, year));
  let sum = OPTION_RENT * Math.min(y, COD);
  if (y > COD) {
    const t = y - COD, whole = Math.floor(t);
    for (let i = 0; i < whole; i++) sum += LEASE_RENT * Math.pow(1 + ESCALATOR, i);
    if (whole < TERM) sum += (t - whole) * LEASE_RENT * Math.pow(1 + ESCALATOR, whole);
  }
  return sum;
}
const totalRent = () => paidBy(COD + TERM);
`;
const api = new Function(`${SRC}; return { OPTION_RENT, LEASE_RENT, ESCALATOR, COD, TERM, CAP, COIN, rentAt, paidBy, totalRent };`)();
export const { OPTION_RENT, LEASE_RENT, ESCALATOR, COD, TERM, CAP, COIN, rentAt, paidBy, totalRent } = api;
export const source = SRC;
