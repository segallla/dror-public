// Fig: how a Stage battery lease pays an industrial landlord.
// Build: node figures/landlord-lease/build.mjs [--light]
import { writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import * as k from "../../.claude/skills/anatomy/kit/iso-kit.mjs";
import { kitScript } from "../../.claude/skills/anatomy/scripts/inline-kit.mjs";
import * as M from "./model.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const theme = process.argv.includes("--light") ? "light" : "dark";
const WIDTH = 640;
const HEIGHT = 430;

// ---------- world plan (units ~ px, z up) ----------
const PLATE = { x: -160, y: -92, w: 320, d: 182, r: 8 };
const PLATE_H = 12, FOOT_H = 5;
const WH = { x: -146, y: -80, w: 146, d: 100, r: 1.5 }, WH_H = 44;
const APRON = { x: -146, y: 20, w: 146, d: 14, r: 0.5 };
const UT = { x: 6, y: -44, w: 18, d: 20, r: 1 }, UT_H = 18;
const SG = { x: 6, y: -18, w: 14, d: 30, r: 1 }, SG_H = 26;
const PAD = { x: 34, y: -70, w: 112, d: 72, r: 2 }, PAD_H = 1.6;
const CT = { x: 44, y: -60, w: 88, d: 26, r: 0.8 }, CT_H = 28;
const PCS = { x: 44, y: -24, w: 30, d: 12, r: 0.8 }, PCS_H = 16;
const MT = { x: 84, y: -24, w: 22, d: 16, r: 0.8 }, MT_H = 15;
const LIFT = 16;
const TRENCH_A = { x: 92, y: -8, w: 6, d: 10, r: 0 };
const TRENCH_B = { x: 20, y: 2, w: 78, d: 6, r: 0 };
const TRAY = [88, 46], COIN_R = 7, COIN_H = 1.8, TRAY_H = 1.6;
const DIAL = [128, 44], DIAL_R = 17, DIAL_Z = 30, DIAL_H = 8, DIAL_TOP = DIAL_Z + DIAL_H;
const STAND = { x: 116, y: 34, w: 24, d: 20, r: 2 }, STAND_H = 6;
const RAIL = { x: -122, y: 63, w: 258, d: 4, r: 1 }, RAIL_H = 2.6;
const STRIP = { x: -124, y: 72, w: 262, d: 8, r: 1 };
const YEAR_U = 11, YEAR0 = -110; // year y sits at x = YEAR0 + y * YEAR_U
const FROM = (-150 * Math.PI) / 180, SPAN = (300 * Math.PI) / 180, FULL = 250000;

const P = k.fitProjection(
  [
    ...k.boxCorners(PLATE, -PLATE_H - FOOT_H, 0),
    ...k.boxCorners(CT, 0, PAD_H + CT_H + LIFT + 7),
    ...k.boxCorners(WH, 0, WH_H + 7),
    [DIAL[0] + DIAL_R, DIAL[1], DIAL_TOP],
  ],
  WIDTH,
  HEIGHT,
  { pad: 22, azimuth: 45 },
);

const at = (p) => k.iso(p, P);
const S = (paths, style) => k.solidSvg(paths, style);
const L = (d, style) => k.lineSvg(d, style);
const D = (points, style) => k.dotsSvg(points, style);
const seg = (a, b) => k.segment(a, b, P);
const closed = (pts) => k.pathOf(pts.map(at), true);
const rectY = (x0, x1, z0, z1, y) => closed([[x0, y, z0], [x1, y, z0], [x1, y, z1], [x0, y, z1]]);
const rectX = (y0, y1, z0, z1, x) => closed([[x, y0, z0], [x, y1, z0], [x, y1, z1], [x, y0, z1]]);
const byDepth = (pts) => [...pts].sort((a, b) => k.depthOf([a[0], a[1], 0], P) - k.depthOf([b[0], b[1], 0], P));
const bandY = (x0, x1, zs, y) => zs.map((z) => seg([x0, y, z], [x1, y, z])).join("");
const bandX = (y0, y1, zs, x) => zs.map((z) => seg([x, y0, z], [x, y1, z])).join("");
const range = (a, b, step) => { const out = []; for (let v = a; v <= b + 1e-9; v += step) out.push(+v.toFixed(3)); return out; };

// ---------- bench ----------
function bench() {
  const out = [`<path class="iso-halo" d="${k.haloOf(PLATE, -PLATE_H - FOOT_H, PLATE_H, P)}"/>`];
  for (const [x, y] of byDepth(k.corners(PLATE, 22))) {
    out.push(S(k.cylinder(x, y, 7, -PLATE_H - FOOT_H, 1.6, P, 28), { tone: "lo" }));
    out.push(S(k.cylinder(x, y, 5.4, -PLATE_H - FOOT_H + 1.6, FOOT_H - 1.6, P, 28), { tone: "mid" }));
  }
  out.push(S(k.slabOf(PLATE, -PLATE_H, PLATE_H, P, 8, 1.6), { tone: "mid", inner: L(k.sideSeam(PLATE, -4, P, 8), { tone: "faint" }) }));
  out.push(L(k.planOutline(k.insetPlan(PLATE, 5), 0, P), { tone: "lo" }));
  const screws = k.corners(PLATE, 10);
  out.push(L(screws.map(([x, y]) => k.ring(x, y, 2.2, 0, P, 16)).join(""), { tone: "lo" }));
  out.push(D(screws.map(([x, y]) => at([x, y, 0])), { size: 0.5 }));
  // label plate
  const label = { x: -150, y: 64, w: 22, d: 15, r: 1 };
  out.push(S(k.slabOf(label, 0, 0.8, P, 4), { tone: "lo", crease: "none" }));
  out.push(L(k.planOutline(k.insetPlan(label, 1.6), 0.8, P, 3), { tone: "faint" }));
  [[4, 15], [4, 12], [4, 9]].forEach(([x0, len], i) => out.push(L(k.lineOnTop([label.x + x0, label.y + 5 + i * 2.6], [label.x + x0 + len, label.y + 5 + i * 2.6], 0.8, P), { tone: "lo", free: true })));
  out.push(D([at([label.x + 2.4, label.y + 2.4, 0.8]), at([label.x + label.w - 2.4, label.y + label.d - 2.4, 0.8])], { size: 0.4 }));
  // year ruler: one minor tick a year, a major every five, year 0 at YEAR0
  out.push(S(k.slabOf(STRIP, 0, 0.6, P, 3), { tone: "lo", crease: "none" }));
  const t = k.topTicks(YEAR0, YEAR0 + 22 * YEAR_U, YEAR_U, 5, STRIP.y + 0.01, 0.6, [2.4, 4.4], P);
  out.push(L(t.minor, { tone: "lo" }), L(t.major, { tone: "mid" }));
  const half = k.topTicks(YEAR0 + YEAR_U / 2, YEAR0 + 22 * YEAR_U, YEAR_U, 1000, STRIP.y + 0.01, 0.6, [1.2, 1.2], P);
  out.push(L(half.minor + half.major, { tone: "faint" }));
  // COD mark: a dot on the ruler at year 2
  out.push(D([at([YEAR0 + 2 * YEAR_U, STRIP.y + 6, 0.6])], { size: 0.9, tone: "hi" }));
  out.push(D([at([STRIP.x + 2, STRIP.y + 4, 0.6]), at([STRIP.x + STRIP.w - 2, STRIP.y + 4, 0.6])], { size: 0.45 }));
  // carriage rail with end stops
  out.push(S(k.slabOf(RAIL, 0, RAIL_H, P, 3, 0.4), { tone: "mid" }));
  out.push(D(range(RAIL.x + 10, RAIL.x + RAIL.w - 10, 40).map((x) => at([x, RAIL.y + 2, RAIL_H])), { size: 0.35, tone: "lo" }));
  for (const x of [RAIL.x - 5, RAIL.x + RAIL.w]) {
    out.push(S(k.slabOf({ x, y: RAIL.y - 2, w: 5, d: 8, r: 1.2 }, 0, 6, P, 3, 0.5), { tone: "mid" }));
    out.push(D([at([x + 2.5, RAIL.y + 2, 6])], { size: 0.45 }));
  }
  return out.join("");
}

// ---------- the landlord's building: untouched ----------
function warehouse() {
  const out = [];
  out.push(S(k.slabOf(APRON, 0, 0.6, P, 2), { tone: "lo", crease: "none" }));
  out.push(L(range(APRON.x + 24, APRON.x + APRON.w - 12, 24).map((x) => k.lineOnTop([x, APRON.y], [x, APRON.y + APRON.d], 0.6, P)).join(""), { tone: "faint" }));
  out.push(`<path class="iso-halo" d="${k.haloOf(k.insetPlan(WH, -2), 0, 0.1, P)}" style="filter:blur(3px)"/>`);
  out.push(S(k.slabOf(WH, 0, WH_H, P, 3, 0.8), { tone: "mid", inner: L(k.sideSeam(WH, WH_H - 3, P, 3), { tone: "lo" }) + L(k.sideSeam(WH, 6, P, 3), { tone: "faint" }) }));
  const Y = WH.y + WH.d, X = WH.x + WH.w;
  // front (+y) face: four dock doors with slats, pilasters between, bumpers
  const doors = [0, 1, 2, 3].map((i) => WH.x + 12 + i * 34);
  doors.forEach((x0) => {
    out.push(L(rectY(x0, x0 + 22, 0, 24, Y), { tone: "lo" }));
    out.push(L(bandY(x0, x0 + 22, range(3, 21, 3), Y), { tone: "faint" }));
    out.push(L(seg([x0 + 11, Y, 0], [x0 + 11, Y, 3]), { tone: "faint" }));
  });
  out.push(L(doors.slice(0, 3).map((x0) => seg([x0 + 28, Y, 6], [x0 + 28, Y, WH_H - 3])).join(""), { tone: "faint" }));
  doors.forEach((x0) => {
    for (const bx of [x0 - 2.6, x0 + 22.6]) out.push(S(k.slabOf({ x: bx, y: Y, w: 2, d: 1.6, r: 0.3 }, 3, 6, P, 2), { tone: "lo", crease: "none" }));
    out.push(D([at([x0 + 11, Y, 27.5])], { size: 0.5, tone: "mid" }));
  });
  // side (+x) face: man door, office window band, conduit stub to the gear
  out.push(L(rectX(6, 14, 0, 16, X), { tone: "lo" }));
  out.push(D([at([X, 12.6, 8])], { size: 0.4 }));
  out.push(L(rectX(-74, -50, 28, 36, X), { tone: "lo" }));
  out.push(L(range(-68, -56, 6).map((y) => seg([X, y, 28], [X, y, 36])).join(""), { tone: "faint" }));
  // roof: deck ribs edge to edge, skylights, three rooftop units
  out.push(L(range(WH.x + 8, X - 8, 8).map((x) => k.lineOnTop([x, WH.y + 0.4], [x, Y - 0.4], WH_H, P)).join(""), { tone: "faint" }));
  for (const [x, y] of [[-132, -48], [-92, -48], [-52, -48], [-132, -20], [-52, -20]]) {
    const sky = { x, y, w: 6, d: 18, r: 0.6 };
    out.push(S(k.slabOf(sky, WH_H, 1.2, P, 2), { tone: "lo", crease: "none" }));
    out.push(L(k.lineOnTop([x + 3, y], [x + 3, y + 18], WH_H + 1.2, P), { tone: "faint" }));
  }
  for (const [x, y] of byDepth([[-118, -72], [-84, -26], [-30, -70]])) {
    const rtu = { x, y, w: 18, d: 13, r: 1 };
    out.push(S(k.slabOf({ x: x - 1, y: y - 1, w: 20, d: 15, r: 1 }, WH_H, 1, P, 2), { tone: "lo", crease: "none" }));
    out.push(S(k.slabOf(rtu, WH_H + 1, 7, P, 3, 0.5), { tone: "mid", inner: L(k.sideSeam(rtu, WH_H + 4, P, 3), { tone: "faint" }) }));
    const [cx, cy] = [x + 12, y + 6.5];
    out.push(L(k.ring(cx, cy, 4.2, WH_H + 8, P, 32) + k.ring(cx, cy, 1, WH_H + 8, P, 12), { tone: "lo" }));
    out.push(L([0, 1, 2, 3].map((i) => { const a = (i * Math.PI) / 2 + 0.4; return k.lineOnTop([cx + Math.cos(a), cy + Math.sin(a)], [cx + Math.cos(a) * 4.2, cy + Math.sin(a) * 4.2], WH_H + 8, P); }).join(""), { tone: "faint" }));
    out.push(D([at([x + 3, y + 3, WH_H + 8]), at([x + 3, y + 10, WH_H + 8])], { size: 0.35, tone: "lo" }));
  }
  return out.join("");
}


// the tenant's trailer at dock 2 and the truck court: the building keeps working
function court() {
  const out = [];
  const curb = { x: WH.x, y: 55, w: 128, d: 2, r: 0.5 };
  out.push(L(range(WH.x + 6, WH.x + 118, 14).map((x) => k.lineOnTop([x, APRON.y + APRON.d], [x, curb.y], 0, P)).join(""), { tone: "faint" }));
  out.push(S(k.slabOf(curb, 0, 0.5, P, 2), { tone: "lo", crease: "none" }));
  const T = { x: WH.x + 47, y: APRON.y + 1.2, w: 20, d: 32, r: 0.6 }, z0 = 6.5, h = 19;
  out.push(`<path class="iso-halo" d="${k.haloOf(k.insetPlan(T, -1), 0, 0.1, P)}" style="filter:blur(2px)"/>`);
  for (const y of [T.y + 3, T.y + 9]) out.push(S(k.slabOf({ x: T.x + 0.5, y, w: T.w - 1, d: 5, r: 2.2 }, 0, 6, P, 4), { tone: "lo", crease: "none", inner: L(k.sideSeam({ x: T.x + 0.5, y, w: T.w - 1, d: 5, r: 2.2 }, 3, P, 4), { tone: "faint" }) }));
  for (const x of [T.x + 3, T.x + T.w - 4.6]) out.push(S(k.slabOf({ x, y: T.y + 24, w: 1.6, d: 1.6, r: 0.3 }, 0, z0, P, 2), { tone: "mid", crease: "none" }));
  out.push(S(k.slabOf(T, z0, h, P, 2, 0.5), { tone: "mid", inner: L(k.sideSeam(T, z0 + 1.6, P, 2) + k.sideSeam(T, z0 + h - 1.6, P, 2), { tone: "lo" }) }));
  const X = T.x + T.w, Y = T.y + T.d;
  out.push(L(range(T.y + 3, Y - 3, 3).map((y) => seg([X, y, z0 + 1.6], [X, y, z0 + h - 1.6])).join(""), { tone: "faint" }));
  out.push(L(rectY(T.x + 3, X - 3, z0 + 4, z0 + h - 4, Y), { tone: "lo" }));
  out.push(D([at([T.x + 2, Y, z0 + h - 1]), at([X - 2, Y, z0 + h - 1])], { size: 0.45, tone: "hi" }));
  return out.join("");
}

// ---------- the site's existing grid connection ----------
function service() {
  const out = [];
  // utility transformer on its pad
  out.push(S(k.slabOf({ x: UT.x - 3, y: UT.y - 3, w: UT.w + 6, d: UT.d + 6, r: 1 }, 0, 1.2, P, 2), { tone: "lo", crease: "none" }));
  out.push(S(k.slabOf(UT, 1.2, UT_H, P, 3, 0.6), { tone: "mid", inner: L(k.sideSeam(UT, 1.2 + UT_H - 3, P, 3), { tone: "faint" }) }));
  const ux = UT.x + UT.w;
  out.push(L(rectX(UT.y + 3, UT.y + UT.d - 3, 4, 14, ux), { tone: "lo" }));
  out.push(L(range(UT.y + 5, UT.y + UT.d - 5, 2).map((y) => seg([ux, y, 4], [ux, y, 14])).join(""), { tone: "faint" }));
  out.push(L(rectY(UT.x + 4, UT.x + UT.w - 4, 5, 13, UT.y + UT.d), { tone: "lo" }));
  out.push(D([at([UT.x + 6, UT.y + UT.d, 11]), at([UT.x + UT.w - 6, UT.y + UT.d, 11])], { size: 0.4 }));
  for (const y of byDepth([[0, UT.y + 5], [0, UT.y + 10], [0, UT.y + 15]]).map((p) => p[1])) {
    out.push(S(k.cylinder(UT.x + 7, y, 1.5, 1.2 + UT_H, 1, P, 14), { tone: "lo" }));
    out.push(S(k.cylinder(UT.x + 7, y, 1, 2.2 + UT_H, 3.4, P, 14), { tone: "hi", crease: "none", inner: L(k.sideArc(UT.x + 7, y, 1, 3.6 + UT_H, P, 10), { tone: "faint" }) }));
  }
  // bus duct transformer -> switchgear
  out.push(S(k.slabOf({ x: 10, y: UT.y + UT.d, w: 6, d: SG.y - UT.y - UT.d, r: 0.4 }, 11, 6, P, 2), { tone: "mid", crease: "none" }));
  // bus duct switchgear -> building wall
  out.push(S(k.slabOf({ x: 0, y: -12, w: SG.x, d: 6, r: 0.4 }, 18, 6, P, 2), { tone: "mid", crease: "none" }));
  // switchgear line-up
  out.push(S(k.slabOf({ x: SG.x - 2, y: SG.y - 2, w: SG.w + 4, d: SG.d + 4, r: 1 }, 0, 1.2, P, 2), { tone: "lo", crease: "none" }));
  out.push(S(k.slabOf(SG, 1.2, SG_H, P, 3, 0.6), { tone: "mid", inner: L(k.sideSeam(SG, 1.2 + SG_H - 3, P, 3), { tone: "faint" }) }));
  const sx = SG.x + SG.w;
  [0, 1, 2].forEach((i) => {
    const y0 = SG.y + 1.5 + i * 9.4;
    out.push(L(rectX(y0, y0 + 8.4, 3, 23, sx), { tone: "lo" }));
    out.push(L(rectX(y0 + 2, y0 + 6.4, 19, 21, sx), { tone: "faint" }));
    out.push(L(rectX(y0 + 2, y0 + 6.4, 5, 7, sx), { tone: "faint" }));
    out.push(D([at([sx, y0 + 7, 13])], { size: 0.45, tone: "hi" }));
  });
  return out.join("");
}

// ---------- the idle yard, leased to Stage ----------
function yard() {
  const out = [];
  out.push(S(k.slabOf(PAD, 0, PAD_H, P, 3, 0.5), { tone: "lo" }));
  out.push(L([PAD.x + 37, PAD.x + 74].map((x) => k.lineOnTop([x, PAD.y], [x, PAD.y + PAD.d], PAD_H, P)).join("") + k.lineOnTop([PAD.x, -30], [PAD.x + PAD.w, -30], PAD_H, P), { tone: "faint" }));
  // anchor bolts that wait for the container
  out.push(D(k.corners(CT, 3).map(([x, y]) => at([x, y, PAD_H])), { size: 0.45, tone: "mid" }));
  out.push(bollard(PAD.x + PAD.w, PAD.y + 2));
  return out.join("");
}

function bollard(x, y) {
  return S(k.cylinder(x, y, 1.8, 0, 11, P, 18), { tone: "mid", inner: L(k.sideArc(x, y, 1.8, 8, P, 12) + k.sideArc(x, y, 1.8, 6.5, P, 12), { tone: "faint" }) });
}

// Stage's assembly: battery container, inverter skid and step-up transformer, built at rest on the pad.
function assembly() {
  const out = [];
  const z0 = PAD_H, top = z0 + CT_H;
  const Y = CT.y + CT.d, X = CT.x + CT.w;
  out.push(S(k.slabOf(CT, z0, CT_H, P, 2, 0.6), { tone: "hi", crease: "lo", inner: L(k.sideSeam(CT, z0 + 2.4, P, 2) + k.sideSeam(CT, top - 2.4, P, 2), { tone: "lo" }) }));
  // corrugated long side, ribs ending on the top and bottom rails
  out.push(L(range(CT.x + 3, X - 3, 2.4).map((x) => seg([x, Y, z0 + 2.4], [x, Y, top - 2.4])).join(""), { tone: "faint" }));
  // label plate and the one engraved name
  out.push(L(rectY(CT.x + 8, CT.x + 30, z0 + 16, z0 + 22, Y + 0.05), { tone: "lo" }));
  out.push(k.faceTextSvg(k.sideMatrix([CT.x + 19, Y + 0.05], z0 + 17.6, P, "left"), "STAGE", { size: 3.4, tone: "mid", anchor: "middle" }));
  // end doors with lock bars and hinges
  out.push(L(rectX(CT.y + 1.6, CT.y + 13, z0 + 2.4, top - 2.4, X) + rectX(CT.y + 13, CT.y + CT.d - 1.6, z0 + 2.4, top - 2.4, X), { tone: "lo" }));
  out.push(L([CT.y + 5, CT.y + 10, CT.y + 16, CT.y + 21].map((y) => seg([X, y, z0 + 2.4], [X, y, top - 2.4])).join(""), { tone: "mid" }));
  out.push(D([7, 14, 21].flatMap((h) => [at([X, CT.y + 2.6, z0 + 2.4 + h]), at([X, CT.y + CT.d - 2.6, z0 + 2.4 + h])]), { size: 0.4, tone: "lo" }));
  out.push(D([at([X, CT.y + 11.6, z0 + 13]), at([X, CT.y + 14.4, z0 + 13])], { size: 0.5, tone: "hi" }));
  // corner castings
  for (const [x, y] of [[CT.x, Y - 2.4], [X - 3, Y - 2.4], [X - 3, CT.y]]) out.push(S(k.slabOf({ x, y, w: 3, d: 2.4, r: 0.3 }, top - 2.4, 2.8, P, 2), { tone: "mid", crease: "none" }));
  // two HVAC units on the roof
  for (const x of [CT.x + 12, CT.x + 56]) {
    const unit = { x, y: CT.y + 5, w: 18, d: 15, r: 1 };
    out.push(S(k.slabOf(unit, top + 0.4, 6, P, 3, 0.5), { tone: "mid" }));
    const [cx, cy] = [x + 9, CT.y + 12.5];
    out.push(L(k.ring(cx, cy, 5, top + 6.4, P, 36) + k.ring(cx, cy, 1.1, top + 6.4, P, 12), { tone: "lo" }));
    out.push(L([0, 1, 2, 3, 4].map((i) => { const a = (i * 2 * Math.PI) / 5; return k.lineOnTop([cx + Math.cos(a) * 1.1, cy + Math.sin(a) * 1.1], [cx + Math.cos(a + 0.5) * 5, cy + Math.sin(a + 0.5) * 5], top + 6.4, P); }).join(""), { tone: "faint" }));
  }
  // status lamp on the long side: dark until COD
  out.push(`<circle data-part="lamp" class="lamp" cx="${at([X - 8, Y, top - 6])[0].toFixed(1)}" cy="${at([X - 8, Y, top - 6])[1].toFixed(1)}" r="1.1"/>`);
  out.push(L(k.sideRing([X - 8, Y, top - 6], 1.8, "y", P, 16), { tone: "lo" }));
  // inverter skid
  out.push(S(k.slabOf(PCS, z0, PCS_H, P, 2, 0.5), { tone: "mid", inner: L(k.sideSeam(PCS, z0 + PCS_H - 2.4, P, 2), { tone: "faint" }) }));
  const py = PCS.y + PCS.d;
  [0, 1].forEach((i) => {
    const x0 = PCS.x + 2 + i * 13.5;
    out.push(L(rectY(x0, x0 + 12.5, z0 + 2, z0 + PCS_H - 4, py), { tone: "lo" }));
    out.push(L(range(z0 + 4, z0 + PCS_H - 6, 1.6).map((z) => rectY(x0 + 2.5, x0 + 10, z, z + 0.5, py)).join(""), { tone: "faint" }));
  });
  // step-up transformer with radiator panel and bushings
  out.push(S(k.slabOf(MT, z0, MT_H, P, 2, 0.5), { tone: "mid", inner: L(k.sideSeam(MT, z0 + MT_H - 2.4, P, 2), { tone: "faint" }) }));
  const my = MT.y + MT.d;
  out.push(L(rectY(MT.x + 2.5, MT.x + MT.w - 2.5, z0 + 2.5, z0 + 11.5, my), { tone: "lo" }));
  out.push(L(range(MT.x + 4.5, MT.x + MT.w - 4.5, 1.8).map((x) => seg([x, my, z0 + 2.5], [x, my, z0 + 11.5])).join(""), { tone: "faint" }));
  for (const x of [MT.x + 6, MT.x + 11, MT.x + 16]) {
    out.push(S(k.cylinder(x, MT.y + 5, 1.4, z0 + MT_H, 1, P, 14), { tone: "lo" }));
    out.push(S(k.cylinder(x, MT.y + 5, 0.9, z0 + MT_H + 1, 3, P, 14), { tone: "hi", crease: "none", inner: L(k.sideArc(x, MT.y + 5, 0.9, z0 + MT_H + 2.4, P, 10), { tone: "faint" }) }));
  }
  return out.join("");
}

// cable trench from Stage's transformer to the landlord's existing switchgear
function trench() {
  const out = [];
  const topZ = PAD_H + 0.8;
  out.push(S(k.slabOf(TRENCH_A, PAD_H, 0.8, P, 2), { tone: "mid", crease: "lo" }));
  out.push(L(range(TRENCH_A.y + 2.5, TRENCH_A.y + TRENCH_A.d - 2.5, 2.5).map((y) => k.lineOnTop([TRENCH_A.x, y], [TRENCH_A.x + TRENCH_A.w, y], topZ, P)).join(""), { tone: "lo" }));
  out.push(S(k.slabOf(TRENCH_B, 0, topZ, P, 2), { tone: "mid", crease: "lo" }));
  out.push(L(range(TRENCH_B.x + 6, TRENCH_B.x + TRENCH_B.w - 6, 6).map((x) => k.lineOnTop([x, TRENCH_B.y], [x, TRENCH_B.y + TRENCH_B.d], topZ, P)).join(""), { tone: "lo" }));
  out.push(D(range(TRENCH_B.x + 3, TRENCH_B.x + TRENCH_B.w - 3, 6).map((x) => at([x, TRENCH_B.y + 3, topZ])), { size: 0.35, tone: "lo" }));
  return out.join("");
}

// ---------- the landlord's take: coin stack and rent gauge ----------
const COINS = Math.ceil(M.totalRent() / M.COIN);
function tray() {
  const [x, y] = TRAY;
  return S(k.cylinder(x, y, COIN_R + 2.4, 0, TRAY_H, P, 48, 0.5), { tone: "lo" }) + L(k.ring(x, y, COIN_R + 0.8, TRAY_H, P, 48), { tone: "faint" });
}
function coin(i) {
  const [x, y] = TRAY, z = TRAY_H + i * COIN_H;
  return S(k.cylinder(x, y, COIN_R, z, COIN_H - 0.15, P, 48, 0.4), { tone: "mid", crease: "lo", inner: L(k.knurl(x, y, COIN_R, z + 0.25, z + COIN_H - 0.4, 54, P, 0.3), { tone: "lo" }) }) + L(k.ring(x, y, COIN_R - 1.6, z + COIN_H - 0.15, P, 40), { tone: "faint" });
}

function gauge() {
  const out = [];
  const [x, y] = DIAL;
  out.push(S(k.slabOf(STAND, 0, STAND_H, P, 4, 0.6), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(STAND, 2.4), STAND_H, P, 3), { tone: "faint" }));
  out.push(D(k.corners(STAND, 3).map(([sx, sy]) => at([sx, sy, STAND_H])), { size: 0.45 }));
  out.push(S(k.cylinder(x, y, 4.2, STAND_H, 2.4, P, 24), { tone: "mid" }));
  out.push(S(k.cylinder(x, y, 2.6, STAND_H + 2.4, DIAL_Z - STAND_H - 2.4, P, 20), { tone: "mid", crease: "none", inner: L(k.sideArc(x, y, 2.6, 18, P, 12), { tone: "faint" }) }));
  out.push(S(k.cylinder(x, y, DIAL_R, DIAL_Z, DIAL_H, P, 64, 0.8), { tone: "hi", crease: "lo", inner: L(k.sideArc(x, y, DIAL_R, DIAL_TOP - 3.2, P, 40), { tone: "faint" }) }));
  out.push(L(k.knurl(x, y, DIAL_R, DIAL_TOP - 3.2, DIAL_TOP, 84, P, 0.3), { tone: "lo" }));
  out.push(L(k.ring(x, y, DIAL_R - 2, DIAL_TOP, P, 64), { tone: "lo" }));
  const ticks = k.radialTicks(x, y, DIAL_R - 2, 50, 5, DIAL_TOP, [1.2, 2.6], P, FROM, SPAN);
  out.push(L(ticks.minor, { tone: "lo" }), L(ticks.major, { tone: "mid" }));
  // the option-rent and first-year marks on the scale
  for (const value of [M.OPTION_RENT, M.LEASE_RENT]) {
    const a = FROM + SPAN * (value / FULL);
    out.push(D([at([x + Math.sin(a) * (DIAL_R - 6.4), y - Math.cos(a) * (DIAL_R - 6.4), DIAL_TOP])], { size: 0.6, tone: "hi" }));
  }
  out.push(L(k.ring(x, y, 1.6, DIAL_TOP, P, 16), { tone: "mid" }));
  // crown on the +x side
  out.push(S(k.slabOf({ x: x + DIAL_R - 1, y: y - 2.2, w: 4.4, d: 4.4, r: 1.2 }, DIAL_Z + 2, 4, P, 3), { tone: "mid", crease: "none" }));
  return out.join("");
}
const needleAt = (frac) => {
  const a = FROM + SPAN * frac;
  const [x, y] = DIAL;
  return k.lineOnTop([x - Math.sin(a) * 3.4, y + Math.cos(a) * 3.4], [x + Math.sin(a) * (DIAL_R - 3.4), y - Math.cos(a) * (DIAL_R - 3.4)], DIAL_TOP + 0.2, P);
};

// year carriage, built at year 0 and moved along x
function carriage() {
  const c = { x: -8, y: RAIL.y - 3, w: 16, d: 10, r: 1.5 };
  const z = RAIL_H;
  const out = [`<path class="iso-halo" d="${k.haloOf(k.insetPlan(c, 2), z, 0.1, P)}" style="filter:blur(3px)"/>`];
  out.push(S(k.slabOf(c, z, 4, P, 4, 0.5), { tone: "mid" }));
  out.push(D([at([c.x + 2.4, c.y + 2.4, z + 4]), at([c.x + c.w - 2.4, c.y + 2.4, z + 4]), at([c.x + 2.4, c.y + c.d - 2.4, z + 4]), at([c.x + c.w - 2.4, c.y + c.d - 2.4, z + 4])], { size: 0.4, tone: "lo" }));
  // pointer tongue reaching over the ruler, its tip mark on the year
  const tongue = { x: -1.6, y: c.y + c.d, w: 3.2, d: 6, r: 0.6 };
  out.push(S(k.slabOf(tongue, z + 0.4, 1, P, 2), { tone: "mid", crease: "none" }));
  out.push(L(k.lineOnTop([0, c.y + c.d + 1], [0, c.y + c.d + 6], z + 1.4, P), { tone: "hi" }));
  // knurled thumb knob
  out.push(S(k.cylinder(0, c.y + 5, 3.2, z + 4, 3.4, P, 28), { tone: "mid", inner: L(k.knurl(0, c.y + 5, 3.2, z + 4.2, z + 7.2, 30, P), { tone: "lo" }) }));
  out.push(D([at([0, c.y + 5, z + 7.4])], { size: 0.5, tone: "hi" }));
  return out.join("");
}

const xOf = (year) => YEAR0 + year * YEAR_U;
const svg = k.figureSvg({
  width: WIDTH,
  height: HEIGHT,
  label:
    "A bench model of an industrial landlord's site. A warehouse with its loading docks stands on the left, untouched, with the site's existing utility transformer and switchgear beside it. On the idle yard to the right, Stage's battery container, inverter and transformer drop onto a concrete pad at the start of operations and tie into the existing switchgear through a cable trench. A carriage on a ruler sets the year of the lease; a dial gauge reads the rent paid that year and a stack of coins grows with the rent collected.",
  body: [
    bench(),
    warehouse(),
    court(),
    service(),
    yard(),
    `<path data-part="shadow" class="iso-halo" d="${[CT, PCS, MT].map((plan) => k.haloOf(k.insetPlan(plan, -1.2), PAD_H, 0.1, P)).join("")}" style="filter:blur(2.5px);opacity:0"/>`,
    `<g data-part="stage" style="opacity:0" transform="${k.translateAlong(P, [0, 0, LIFT])}">${assembly()}</g>`,
    `<g data-part="trench" style="opacity:0">${trench()}</g>`,
    bollard(PAD.x + 2, 12),
    bollard(PAD.x + PAD.w, 8),
    tray(),
    ...Array.from({ length: COINS }, (_, i) => `<g data-part="coin" style="opacity:0">${coin(i)}</g>`),
    gauge(),
    `<path data-part="needle" class="iso-line" data-tone="lit" data-free="start" d="${needleAt(M.rentAt(0) / FULL)}" style="stroke-width:1.1"/>`,
    `<g data-part="carriage" transform="${k.translateAlong(P, [xOf(0), 0, 0])}">${carriage()}</g>`,
  ],
});

const live = `
const P = ${JSON.stringify(P)};
const DIAL = ${JSON.stringify(DIAL)}, DIAL_R = ${DIAL_R}, DIAL_TOP = ${DIAL_TOP}, FROM = ${FROM}, SPAN = ${SPAN}, FULL = ${FULL};
const LIFT = ${LIFT}, YEAR0 = ${YEAR0}, YEAR_U = ${YEAR_U}, END = ${M.COD + M.TERM}, COIN_H = ${COIN_H};
${M.source}
const needleAt = ${needleAt.toString().replace("k.lineOnTop", "lineOnTop")};
const stage = document.querySelector(".iso-stage");
const svg = stage.querySelector("svg");
const $ = (name) => svg.querySelector('[data-part="' + name + '"]');
const carriage = $("carriage"), needle = $("needle"), group = $("stage"), trench = $("trench"), shadow = $("shadow"), lamp = $("lamp");
const coins = [...svg.querySelectorAll('[data-part="coin"]')];
const readout = document.querySelector("[data-readout]");
const still = matchMedia("(prefers-reduced-motion: reduce)");
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const smooth = (a, b, v) => { const t = clamp((v - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); };
const money = (v) => v >= 995000 ? "$" + (v / 1e6).toFixed(2) + "M" : "$" + Math.round(v / 1000) + "k";
let year = 0, target = 0, dial = { at: rentAt(0), rate: 0 };
let frame = 0, last = 0, clock = 0, touring = !still.matches, visible = false, idle = 0;
// tour: one year a second across the lease, a pause at the end, then back to the start
const tourAt = (t) => { const span = END + 4; const u = t % span; return u < 1.2 ? 0 : Math.min(END, u - 1.2); };
function draw() {
  const x = YEAR0 + year * YEAR_U;
  carriage.setAttribute("transform", translateAlong(P, [x, 0, 0]));
  const land = smooth(COD - 0.9, COD, year);
  group.setAttribute("transform", translateAlong(P, [0, 0, LIFT * (1 - land) * (1 - land)]));
  group.style.opacity = smooth(COD - 1, COD - 0.45, year).toFixed(3);
  shadow.style.opacity = (land * land).toFixed(3);
  const live = smooth(COD, COD + 0.25, year);
  trench.style.opacity = live.toFixed(3);
  lamp.style.opacity = live.toFixed(3);
  needle.setAttribute("d", needleAt(clamp(dial.at / FULL, 0, 1)));
  const sum = paidBy(year);
  coins.forEach((c, i) => {
    const a = clamp(sum / COIN - i, 0, 1);
    c.style.opacity = smooth(0.55, 1, a).toFixed(3);
  });
  const n = Math.min(END, Math.floor(year) + 1);
  const phase = year < COD ? "option rent " : "battery rent ";
  const text = "Year " + n + " · " + phase + money(rentAt(year)) + "/yr · " + money(sum) + " to date";
  if (readout.textContent !== text) readout.textContent = text;
  stage.setAttribute("aria-valuenow", String(n));
  stage.setAttribute("aria-valuetext", text);
}
function tick(now) {
  const dt = last ? Math.min((now - last) / 1000, 1 / 30) : 1 / 60;
  last = now;
  const calm = still.matches;
  if (touring) { clock += dt; target = tourAt(clock); }
  const back = target < year - 2;
  year = calm ? target : year + (target - year) * (1 - Math.exp(-dt / (back ? 0.5 : 0.22)));
  if (Math.abs(target - year) < 0.002) year = target;
  const want = rentAt(year);
  const k = 90, c = calm ? 2 * Math.sqrt(90) : 13;
  for (let i = 0; i < 4; i++) { dial.rate += ((want - dial.at) * k - dial.rate * c) * dt / 4; dial.at += dial.rate * dt / 4; }
  if (calm || (Math.abs(want - dial.at) < 20 && Math.abs(dial.rate) < 20)) { dial.at = want; dial.rate = 0; }
  draw();
  const settled = !touring && year === target && dial.rate === 0;
  frame = visible && !settled ? requestAnimationFrame(tick) : 0;
}
const run = () => { if (!frame && visible) { last = 0; frame = requestAnimationFrame(tick); } };
const steer = (next) => { touring = false; target = clamp(next, 0, END); clearTimeout(idle); idle = setTimeout(() => { touring = !still.matches; clock = target + 1.2; run(); }, 4000); run(); };
new IntersectionObserver((e) => { visible = e[e.length - 1].isIntersecting; if (visible) run(); }, { rootMargin: "120px 0px" }).observe(stage);
stage.addEventListener("pointermove", (event) => {
  const box = svg.getBoundingClientRect();
  steer(clamp(((event.clientX - box.left) / box.width - 0.12) / 0.76, 0, 1) * END);
});
stage.addEventListener("pointerleave", () => steer(target));
stage.addEventListener("keydown", (event) => {
  let to = null;
  if (event.key === "ArrowRight" || event.key === "ArrowUp") to = Math.floor(target + 1e-6) + 1;
  if (event.key === "ArrowLeft" || event.key === "ArrowDown") to = Math.ceil(target - 1e-6) - 1;
  if (event.key === "Home") to = 0;
  if (event.key === "End") to = END;
  if (to === null) return;
  event.preventDefault();
  steer(to);
});
if (still.matches) { year = target = COD + 5; dial.at = rentAt(year); }
draw();
`;

const total = M.totalRent();
const fmtM = (v) => "$" + (v / 1e6).toFixed(1) + "M";
const css = `<style>.lamp{fill:var(--anatomy-lit)}.iso-stage{outline:none;touch-action:pan-y}.iso-stage:focus-visible{box-shadow:0 0 0 1px var(--anatomy-mid);border-radius:8px}</style>`;
const body =
  css +
  k.plateHtml({
    fig: "Fig 1",
    title: "Stage battery lease · landlord",
    hint: "Hover or press ← → to change the year",
    readout: `Year 1 · option rent $60k/yr · $0k to date`,
    keys: [
      { mark: "lit", label: "Needle: rent the landlord receives that year" },
      { mark: "raised", label: "Stage's battery, inverter and transformer, on the idle yard" },
      { mark: "edge", label: `Coins: $${M.COIN / 1000}k of rent collected each` },
    ],
    caption: `The building and its tenant stay exactly as they are. Stage leases only the idle yard and the spare capacity of the grid connection the site already has. For the ${M.COD} development years the landlord collects $${M.OPTION_RENT / 1000}k a year of option rent; at COD the battery lands on its pad and ties into the existing switchgear through a cable trench, and rent steps to $${M.LEASE_RENT / 1000}k a year, rising ${M.ESCALATOR * 100}% a year for ${M.TERM} years. That is about ${fmtM(total)} over the term, and the landlord funds none of the equipment. At a ${(M.CAP * 100).toFixed(1)}% cap rate, the first year of battery rent alone adds about ${fmtM(M.LEASE_RENT / M.CAP)} to the property's value. Terms are the lease defaults in Stage's MORE Power Fund I model, shown for illustration.`,
    body: `<div class="iso-stage" tabindex="0" role="slider" aria-label="Lease year: arrow keys move one year" aria-valuemin="1" aria-valuemax="${M.COD + M.TERM}" aria-valuenow="1">${svg}</div>`,
  });

const themeScript = `try{const b=document.body;if(!b.dataset.fixed&&matchMedia("(prefers-color-scheme: light)").matches&&${theme === "dark" ? "!location.search.includes('dark')" : "false"})b.dataset.theme="light"}catch(e){}`;
const out = theme === "light" ? "landlord-lease-light.html" : "landlord-lease.html";
writeFileSync(join(HERE, out), k.pageHtml({ title: "Landlord Battery Lease", theme, body, script: themeScript + kitScript() + live, width: 720 }));
console.log("wrote", out, "coins", COINS, "total", Math.round(total));
