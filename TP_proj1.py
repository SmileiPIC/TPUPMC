output_every=1
n_part=10

Main(
    geometry = "1Dcartesian",
    interpolation_order = 2,
    simulation_time = 10*2*math.pi,
    timestep = 0.18,
    grid_length  = [4],
    cell_length = [0.2],
    number_of_patches = [ 1 ],
    print_every = output_every,
    EM_boundary_conditions = [['periodic']]
)

Species(
    name = 'ion',
    number_density = 1.0,
    position_initialization = 'regular',
    momentum_initialization = 'cold',
    particles_per_cell = n_part,
    mass = 1836.0,
    charge = 1.0,
    time_frozen = 10000.0,
    boundary_conditions = [['periodic']]
)

Species(
    name = "eon",
    position_initialization = "regular",
    momentum_initialization = "cold",
    particles_per_cell = n_part,
    mass = 1.0,
    charge = -1.0,
    number_density = cosine(1,xamplitude=0.01,xnumber=1),
    boundary_conditions = [['periodic']]
)

DiagScalar (
    precision = 3,
    every = output_every,
    vars = ['Utot', 'Ukin', 'Uelm', 'Ukin_eon', 'Ntot_eon', 'Uelm_Ex']
) 
 
DiagParticleBinning(
    deposited_quantity = "weight",
    every = output_every,
    species = ["eon"],
    axes = [
        ["x", 0., Main.grid_length[0], 100],
        ["px", -0.01, 0.01, 100]
    ]
)

DiagFields(
    every = output_every,
    fields = ['Jx', 'Rho_eon']
)


