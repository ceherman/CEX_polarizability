#!/bin/bash

# Note I don't think this is necessary with my current TIP3P file

cd w1500

# Denote OH2 with the temperature factor (in preparation for cavity formation simulations)

awk '/OH2/ {$10 = 1.00}
           {if ($1=="ATOM")
                printf "%-6s%5.0f%2s%-4s%4s%5.0f%4s%8.3f%8.3f%8.3f%6.2f%6.2f%10s\n",
                $1, $2, "  ", $3, $4, $5, "    ", $6, $7, $8, $9, $10, $11;
            else print}' starting.pdb > equilibrate.x

cd ../
