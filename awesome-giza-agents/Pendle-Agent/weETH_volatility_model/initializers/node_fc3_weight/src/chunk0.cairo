use orion::numbers::{FixedTrait, FP16x16};

fn compute(ref a: Array<FP16x16>) {
a.append(FP16x16 { mag: 3888, sign: true });
a.append(FP16x16 { mag: 11891, sign: false });
a.append(FP16x16 { mag: 9467, sign: false });
a.append(FP16x16 { mag: 25989, sign: true });
a.append(FP16x16 { mag: 4825, sign: false });
a.append(FP16x16 { mag: 16210, sign: true });
a.append(FP16x16 { mag: 15012, sign: true });
a.append(FP16x16 { mag: 23386, sign: true });
a.append(FP16x16 { mag: 9753, sign: false });
a.append(FP16x16 { mag: 22886, sign: true });
a.append(FP16x16 { mag: 15832, sign: true });
a.append(FP16x16 { mag: 11880, sign: false });
a.append(FP16x16 { mag: 9949, sign: false });
a.append(FP16x16 { mag: 18607, sign: true });
a.append(FP16x16 { mag: 9724, sign: true });
a.append(FP16x16 { mag: 22163, sign: true });
}