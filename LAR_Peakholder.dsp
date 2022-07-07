// FAUST standard library
import("stdfaust.lib");


// Peakholder IIR - Loop Stage
	Peakholder = _ : abs <: loop ~_
		with{
			loop = ((_,_) : max);
		};

// Counterbalancing
	LARPeakholder = _ <: *(1-Peakholder);

process = LARPeakholder;
