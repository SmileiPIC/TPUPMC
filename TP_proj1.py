output_every=10
n_part=10

Main(
    geometry = "1d3v",
    interpolation_order = 2,
    sim_time = 30.0,
    timestep = 0.01,
    sim_length  = [1.0],
    cell_length = [0.01],
    number_of_patches = [ 2 ],
    print_every = output_every,
    bc_em_type_x = ['silver-muller'],
)

Species(
    species_type = 'ion',
    nb_density = 1.0,
    initPosition_type = 'regular',
    initMomentum_type = 'cold',
    n_part_per_cell = n_part,
    mass = 1836.0,
    charge = 1.0,
    time_frozen = 10000.0,
    bc_part_type_xmin = 'none',
    bc_part_type_xmax = 'none'
)

Species(
    species_type = "eon",
    initPosition_type = "regular",
    initMomentum_type = "cold",
    n_part_per_cell = n_part,
    mass = 1.0,
    charge = -1.0,
    nb_density = cosine(1,xamplitude=0.1,xnumber=1),
    bc_part_type_xmin = "none",
    bc_part_type_xmax = "none"
)

DiagScalar (
    precision = 3,
    every = output_every,
    vars = ['Utot', 'Ukin', 'Uelm', 'Ukin_eon', 'Ntot_eon', 'Uelm_Ex']
) 
 
DiagParticles(
    output = "density",
    every = output_every,
    species = ["eon"],
    axes = [
        ["x", 0., 1., 100],
        ["px", -0.04, 0.04, 100]
    ]
)

DiagFields(
    every = output_every,
    fields = ['Jx', 'Rho_eon']
)


