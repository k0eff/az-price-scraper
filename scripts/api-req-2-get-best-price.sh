#!/bin/sh
curl --location --request GET 'localhost:8000/price?mincpu=4&maxcpu=8&minram=2&maxram=32&os=linux&excluded=A,Av2&spot=t&region=europe-north'