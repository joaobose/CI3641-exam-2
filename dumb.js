const carnet = '17-10490'.split('').reverse();

const V = {
  X: Number(carnet[2]),
  Y: Number(carnet[1]),
  Z: Number(carnet[0])
};
console.log(V);
const { X, Y, Z } = V;
