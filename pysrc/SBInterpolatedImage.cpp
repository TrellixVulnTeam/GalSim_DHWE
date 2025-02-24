/* -*- c++ -*-
 * Copyright (c) 2012-2022 by the GalSim developers team on GitHub
 * https://github.com/GalSim-developers
 *
 * This file is part of GalSim: The modular galaxy image simulation toolkit.
 * https://github.com/GalSim-developers/GalSim
 *
 * GalSim is free software: redistribution and use in source and binary forms,
 * with or without modification, are permitted provided that the following
 * conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice, this
 *    list of conditions, and the disclaimer given in the accompanying LICENSE
 *    file.
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions, and the disclaimer given in the documentation
 *    and/or other materials provided with the distribution.
 */

#include "PyBind11Helper.h"
#include "SBInterpolatedImage.h"

namespace galsim {

    void pyExportSBInterpolatedImage(py::module& _galsim)
    {
        py::class_<SBInterpolatedImage, SBProfile>(_galsim, "SBInterpolatedImage")
            .def(py::init<const BaseImage<double>&, const Bounds<int>&, const Bounds<int>&,
                 const Interpolant&, const Interpolant&, double, double, GSParams>())
            .def("calculateMaxK", &SBInterpolatedImage::calculateMaxK);

        py::class_<SBInterpolatedKImage, SBProfile>(_galsim, "SBInterpolatedKImage")
            .def(py::init<const BaseImage<std::complex<double> > &,
                 double, const Interpolant&, GSParams>());

        _galsim.def("CalculateSizeContainingFlux", &CalculateSizeContainingFlux);
    }

} // namespace galsim
