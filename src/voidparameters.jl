module VoidParameters
export MeshParams, SphericalVoidParams

using Parameters

@with_kw mutable struct MeshParams
    save_mesh::Bool = true
    dtype::String = "f8"
    nbins::Int = 512
    is_box::Bool = true  # set to false for survey-like data
    box_length::Float64 = 1.  # box length (disregarded if is_box=false)
    box_centre::Array{Float64,1} = fill(box_length/2, 3) # box centre (disregarded if is_box=false)
    padding::Float64 = 1.2  # box padding (disregarded if is_box=true)

    # reconstruction parameters
    recon_alg::String = "IFFTparticle"
    los::String = "z"  # line-of-sight axis of box (disregarded if is_box=false)
    r_smooth::Float64 = box_length/nbins
    omega_m::Float64 = 0.31
    f::Float64 = 0.8
    bias::Float64 = 2.
end

@with_kw mutable struct SphericalVoidParams
    verbose::Bool = false
    output_fn::String = "void_cat_spherical"
    radii::Array{Float64,1}
    min_dens_cut::Float64 = 1.0
    max_overlap_frac::Float64 = 0.
end


end
