package discord

import "time"

var VehicleAirDict = map[string]string{
	"f_16c_block_50": "F-16C Block 50",
	"f_15c_msip2":    "F-15C \"MSIP II\"",
}

var VehicleGroundDict = map[string]string{
	"jp_type_90b_camo":           "Type 90 (B) \"Fuji\"",
	"germ_leopard_2a4m_can":      "Leopard 2A4M CAN",
	"germ_leopard_2a7v":          "Leopard 2A7V",
	"germ_leopard_2a5_pso":       "Leopard 2 PSO",
	"us_m1128_wolfpack":          "M1128 Wolfpack",
	"us_m1a1_hc_usmc":            "M1A1 Click-Bait",
	"germ_leopard_2a4_pzbtl_123": "Leopard 2 (PzBtl 123)",
}

var GameTime = time.Now()
