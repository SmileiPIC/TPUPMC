output_every=10
n_part=100
velocity=0.1
amplitude=0.001
length = 1.68

Main(
    geometry = "1Dcartesian",
    interpolation_order = 2,
    simulation_time = 10.0*2*math.pi,
    timestep = 0.01,
    grid_length = [length],
    cell_length = [length/32],
    number_of_patches = [ 1 ],
    print_every = output_every,
    EM_boundary_conditions = [['periodic']],
    poisson_max_iteration=0
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
    name = "eon1",
    position_initialization = "regular",
    momentum_initialization = "cold",
    particles_per_cell = n_part/2,
    mass = 1.0,
    charge = -1.0,
    number_density = cosine(0.5,xamplitude=amplitude,xnumber=1),
    boundary_conditions = [['periodic']],
    mean_velocity = [velocity, 0, 0] 
)

Species(
    name = "eon2",
    position_initialization = "regular",
    momentum_initialization = "cold",
    particles_per_cell = n_part/2,
    mass = 1.0,
    charge = -1.0,
    number_density = cosine(0.5,xamplitude=amplitude,xnumber=1),
    boundary_conditions = [['periodic']],
    mean_velocity = [-velocity, 0, 0] 
)

DiagScalar (
    precision = 3,
    every=output_every,
    vars = ['Utot', 'Ukin', 'Uelm', 'Ukin_eon1', 'Ukin_eon2', 'Uelm_Ex']
)
 
DiagParticleBinning(
    deposited_quantity = "weight",
    every = output_every,
    species = ['eon1', 'eon2'],
    axes = [
        ["x", 0., length, 100],
        ["px", -4*velocity, 4*velocity, 100]
    ]
)

DiagFields(
    every = output_every,
    fields = ['Jx', 'Rho_eon1', 'Rho_eon2']
)

