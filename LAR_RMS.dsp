// FAUST standard library
import("stdfaust.lib");

// RMS with indipendent attack and release time
RMS(att,rel,x) = loop ~ _ : sqrt
    with {
        loop(y) = (1.0 - coeff) * x * x + coeff * y
            with {
                attCoeff = exp(-2.0 * ma.PI * ma.T / att);
                relCoeff = exp(-2.0 * ma.PI * ma.T / rel);
                coeff = ba.if(abs(x) > y, attCoeff, relCoeff);
            };
    };
// Counterbalancing
LARRMS(att,rel,z) = z*(1-(z:RMS(att,rel)));
process = LARRMS(0.01,0.01) <: _,_;
