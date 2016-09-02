# SIMULATION TP_proj1.py

my_every=10
npart=10

Main(
    geometry = "1d3v",
    interpolation_order = 2,
    sim_time = 30.0,
    cell_length = [0.01],
    timestep = 0.01,
    sim_length  = [1.0],
    number_of_patches = [ 2 ],
    print_every = my_every,
    bc_em_type_x = ['silver-muller'],
)

Species(
	species_type = 'ion',
    nb_density = 1.0,
	initPosition_type = 'regular',
	initMomentum_type = 'cold',
	n_part_per_cell = npart,
	mass = 1836.0,
	charge = 1.0,
	time_frozen = 10000.0,
	bc_part_type_west = 'none',
	bc_part_type_east = 'none'
)

Species(
	species_type = "eon",
	initPosition_type = "regular",
	initMomentum_type = "cold",
	n_part_per_cell = npart,
	mass = 1.0,
	charge = -1.0,
	nb_density = cosine(1,xamplitude=0.1,xnumber=1),
	bc_part_type_west = "none",
	bc_part_type_east = "none"
)

DiagScalar (
 	precision = 3,
	every = my_every,
	vars = ['Utot', 'Ukin', 'Uelm', 'Ukin_eon', 'Ntot_eon', 'Uelm_Ex']
) 
 
DiagParticles(
	output = "density",
	every = my_every,
	species = ["eon"],
	axes = [
		["x", 0., 1., 100],
		["px", -0.04, 0.04, 100]
	]
)

DiagFields(
    every = my_every,
    fields = ['Jx', 'Rho_eon']
)


