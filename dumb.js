const carnet = '17-10490'.split('').reverse();

const V = {
  X: Number(carnet[2]),
  Y: Number(carnet[1]),
  Z: Number(carnet[0])
};
console.log(V);
const { X, Y, Z } = V;

// Pregunta 4
const P4 = {
  A: 2 * ((X + Y) % 5) + 3,
  B: 2 * ((Y + Z) % 5) + 3
};
console.log(P4);
