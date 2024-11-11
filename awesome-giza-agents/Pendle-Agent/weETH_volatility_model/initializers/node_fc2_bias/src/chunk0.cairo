use orion::numbers::{FixedTrait, FP16x16};

fn compute(ref a: Array<FP16x16>) {
a.append(FP16x16 { mag: 238, sign: true });
a.append(FP16x16 { mag: 11212, sign: true });
a.append(FP16x16 { mag: 7069, sign: true });
a.append(FP16x16 { mag: 7491, sign: false });
a.append(FP16x16 { mag: 3005, sign: false });
a.append(FP16x16 { mag: 127, sign: true });
a.append(FP16x16 { mag: 8541, sign: false });
a.append(FP16x16 { mag: 11814, sign: false });
a.append(FP16x16 { mag: 20, sign: false });
a.append(FP16x16 { mag: 15397, sign: false });
a.append(FP16x16 { mag: 8405, sign: false });
a.append(FP16x16 { mag: 249, sign: false });
a.append(FP16x16 { mag: 4953, sign: false });
a.append(FP16x16 { mag: 6915, sign: false });
a.append(FP16x16 { mag: 14577, sign: false });
a.append(FP16x16 { mag: 4276, sign: false });
}