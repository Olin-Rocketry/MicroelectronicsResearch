#------------------------------------------------------------------------------
#
# C5N SCMOS3ME_SUBM scalable design rules from MOSIS with lambda = 0.3um.
#
#------------------------------------------------------------------------------
def printErrors(msg):
    n = geomGetCount()
    if n>0:
        print n, msg

# Initialize the DRC package.
from ui import *
cv = ui().getEditCellView()
lib = cv.lib()

geomBegin(cv)

LAMBDA = 0.3
EPSILON = 0.
#EPSILON = 2./float(lib.dbuPerUU())

# Get raw layers.
nwell = geomGetShapes('nwell', 'drawing')
active = geomGetShapes('active', 'drawing')
poly = geomGetShapes('poly', 'drawing')
nselect = geomGetShapes('nselect', 'drawing')
pselect = geomGetShapes('pselect', 'drawing')
poly2 = geomGetShapes('poly2', 'drawing')
hires = geomGetShapes('hires', 'drawing')
contact = geomGetShapes('contact', 'drawing')
polycontact = geomGetShapes('polycontact', 'drawing')
activecontact = geomGetShapes('activecontact', 'drawing')
poly2contact = geomGetShapes('poly2contact', 'drawing')
metal1 = geomGetShapes('metal1', 'drawing')
via = geomGetShapes('via', 'drawing')
metal2 = geomGetShapes('metal2', 'drawing')
via2 = geomGetShapes('via2', 'drawing')
metal3 = geomGetShapes('metal3', 'drawing')
glass = geomGetShapes('glass', 'drawing')
pads = geomGetShapes('pads', 'drawing')
cap_id = geomGetShapes('cap_id', 'drawing')
res_id = geomGetShapes('res_id', 'drawing')
diode_id = geomGetShapes('diode_id', 'drawing')

# Form derived layers.
gate = geomAnd(poly, active)
ngate = geomAnd(gate, nselect)
pgate = geomAnd(gate, pselect)
diff = geomAndNot(active, gate)
ndiff = geomAnd(diff, nselect)
pdiff = geomAnd(diff, pselect)
nsrcdrain = geomAndNot(ndiff, nwell)
psrcdrain = geomAnd(pdiff, nwell)
nplug = geomAnd(ndiff, nwell)
pplug = geomAndNot(pdiff, nwell)
activecon = geomOr(geomAnd(contact, active), activecontact)
polycon = geomOr(geomAnd(contact, poly), polycontact)
poly2con = geomOr(geomAnd(contact, poly2), poly2contact)
poly2_for_cap = geomAnd(poly2, cap_id)
poly2_for_res = geomAnd(poly2, hires)
poly2_for_tran = geomAndNot(poly2, geomOr(cap_id, hires))
poly2con_on_cap = geomAnd(poly2con, cap_id)
allcon = geomOr(geomOr(contact, activecontact), geomOr(polycontact, poly2contact))
bonding_passivation = geomAnd(glass, pads)
probe_passivation = geomAndNot(glass, pads)
pad_metal = geomAnd(metal3, pads)

# Form connectivity.
geomConnect([[nplug, nwell, ndiff], 
             [activecon, ndiff, pdiff, metal1], 
             [polycon, poly, metal1], 
             [poly2con, poly2, poly2_for_cap, poly2_for_tran, metal1], 
             [via, metal1, metal2], 
             [via2, metal2, metal3],
             [pads, metal3, pad_metal]])

# Check design rules.
print 'Checking for off-grid geometry...'
off_grid_msg = 'Design grid is {0!s}um x {1!s}um'.format(0.5*LAMBDA, 0.5*LAMBDA)
geomOffGrid(nwell, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(active, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(poly, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(nselect, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(pselect, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(poly2, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(hires, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(contact, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(polycontact, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(activecontact, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(poly2contact, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(metal1, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(via, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(metal2, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(via2, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(metal3, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(glass, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(pads, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(cap_id, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(res_id, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(diode_id, 0.5*LAMBDA, LAMBDA, off_grid_msg)

print 'Checking for bad contacts...'
saveDerived(geomAndNot(contact, geomOr(active, geomOr(poly, poly2))), 'Contacts must be enclosed by active, poly, or poly2')

print 'Checking for unselected active...'
saveDerived(geomAndNot(active, geomOr(nselect, pselect)), 'Active must be selected')

#print 'Checking for unplugged wells...'
#plugged_nwell = geomOverlapping(nplug, nwell)
#saveDerived(geomAndNot(nwell, plugged_nwell), 'Wells must be plugged')

#print 'Checking for disconnected abutted substrate/well plugs...'
#geomSpace(nplug, psrcdrain, 4*LAMBDA - EPSILON, diffnet, 'Abutted well plugs must be shorted to the abutting source/drain region')
#geomSpace(pplug, nsrcdrain, 4*LAMBDA - EPSILON, diffnet, 'Abutted substrate plugs must be shorted to the abutting source/drain region')
#geomSpace(ndiff, pdiff, 4*LAMBDA - EPSILON, diffnet, 'Abutted substrate plugs must be shorted to the adjoining source/drain region')

print 'Checking well rules...'
geomWidth(nwell, 12*LAMBDA - EPSILON, '1.1 Well width >= 12')
geomSpace(nwell, 18*LAMBDA - EPSILON, diffnet, '1.2 Spacing between wells at different potentials >= 18')
geomSpace(nwell, 6*LAMBDA - EPSILON, samenet, '1.3 Spacing between wells at same potential >= 6')
geomNotch(nwell, 6*LAMBDA - EPSILON, '1.3 Spacing between wells at same potential >= 6')

print 'Checking active rules...'
geomWidth(active, 3*LAMBDA - EPSILON, '2.1 Active width >= 3')
geomSpace(active, 3*LAMBDA - EPSILON, 0, '2.2 Active spacing >= 3')
geomNotch(active, 3*LAMBDA - EPSILON, '2.2 Active spacing >= 3')
geomEnclose(nwell, psrcdrain, 6*LAMBDA - EPSILON, '2.3 Source/drain active to well edge >= 6')
geomSpace(nwell, nsrcdrain, 6*LAMBDA - EPSILON, 0, '2.3 Source/drain active to well edge >= 6')
geomEnclose(nwell, nplug, 3*LAMBDA - EPSILON, '2.4 Substrate/well contact active to well edge >= 3')
geomSpace(nwell, pplug, 3*LAMBDA - EPSILON, 0, '2.4 Substrate/well contact active to well edge >= 3')
geomSpace(ndiff, geomAvoiding(ndiff, pdiff), 4*LAMBDA - EPSILON, 0, '2.5 Spacing between non-abutting active of different implant >= 4')

print 'Checking poly rules...'
geomWidth(poly, 2*LAMBDA - EPSILON, '3.1 Poly width >= 2')
geomSpace(poly, 3*LAMBDA - EPSILON, 0, '3.2 Poly spacing >= 3')
geomNotch(poly, 3*LAMBDA - EPSILON, '3.2 Poly spacing >= 3')
geomExtension(poly, active, 2*LAMBDA - EPSILON, '3.3 Poly extension of active >= 2')
geomExtension(active, poly, 3*LAMBDA - EPSILON, '3.4 Active extension of poly >= 3')
geomSpace(poly, active, LAMBDA - EPSILON, 0, '3.5 Field poly to active spacing >= 1')

print 'Checking select rules...'
geomSpace(nselect, pgate, 3*LAMBDA - EPSILON, 0, '4.1 Select spacing to channel of tranistor to ensure adequate source/drain width >= 3')
geomSpace(pselect, ngate, 3*LAMBDA - EPSILON, 0, '4.1 Select spacing to channel of tranistor to ensure adequate source/drain width >= 3')
geomOverlap(nselect, active, 2*LAMBDA - EPSILON, '4.2 Select overlap of active >= 2')
geomOverlap(pselect, active, 2*LAMBDA - EPSILON, '4.2 Select overlap of active >= 2')
geomEnclose(nselect, activecon, LAMBDA - EPSILON, '4.3 Select overlap of contact >= 1')
geomEnclose(pselect, activecon, LAMBDA - EPSILON, '4.3 Select overlap of contact >= 1')
geomWidth(nselect, 2*LAMBDA - EPSILON, '4.4 Select width and spacing >= 2 (Note: P-select and N-select may be coincident, but must not overlap)')
geomWidth(pselect, 2*LAMBDA - EPSILON, '4.4 Select width and spacing >= 2 (Note: P-select and N-select may be coincident, but must not overlap)')
geomSpace(nselect, 2*LAMBDA - EPSILON, 0, '4.4 Select width and spacing >= 2 (Note: P-select and N-select may be coincident, but must not overlap)')
geomSpace(pselect, 2*LAMBDA - EPSILON, 0, '4.4 Select width and spacing >= 2 (Note: P-select and N-select may be coincident, but must not overlap)')
geomNotch(nselect, 2*LAMBDA - EPSILON, '4.4 Select width and spacing >= 2 (Note: P-select and N-select may be coincident, but must not overlap)')
geomNotch(pselect, 2*LAMBDA - EPSILON, '4.4 Select width and spacing >= 2 (Note: P-select and N-select may be coincident, but must not overlap)')
saveDerived(geomAnd(nselect, pselect), '4.4 Select width and spacing >= 2 (Note: P-select and N-select may be coincident, but must not overlap)')

print 'Checking poly2 for capacitor rules...'
geomWidth(poly2_for_cap, 7*LAMBDA - EPSILON, '11.1 Poly2 for capacitor width >= 7')
geomSpace(poly2_for_cap, 3*LAMBDA - EPSILON, 0, '11.2 Poly2 for capacitor spacing >= 3')
geomNotch(poly2_for_cap, 3*LAMBDA - EPSILON, '11.2 Poly2 for capacitor spacing >= 3')
geomEnclose(poly, poly2_for_cap, 5*LAMBDA - EPSILON, '11.3 Poly overlap of poly2 for capacitor >= 5')
geomSpace(poly2_for_cap, active, 2*LAMBDA - EPSILON, 0, '11.4 Poly2 for capacitor spacing to active or well edge >= 2')
geomSpace(geomAndNot(poly2_for_cap, nwell), nwell, 2*LAMBDA - EPSILON, 0, '11.4 Poly2 for capacitor spacing to active or well edge >= 2')
geomEnclose(nwell, geomAnd(poly2_for_cap, nwell), 2*LAMBDA - EPSILON, '11.4 Poly2 for capacitor spacing to active or well edge >= 2')
geomSpace(poly2_for_cap, polycon, 6*LAMBDA - EPSILON, 0, '11.5 Poly2 for capacitor spacing to poly contact >= 6')
#geomSpace(poly2_for_cap, metal1, 2*LAMBDA - EPSILON, diffnet, '11.6 Poly2 for capacitor spacing to unrelated metal >= 2')
#geomSpace(poly2_for_cap, metal2, 2*LAMBDA - EPSILON, diffnet, '11.6 Poly2 for capacitor spacing to unrelated metal >= 2')
#geomSpace(poly2_for_cap, metal3, 2*LAMBDA - EPSILON, diffnet, '11.6 Poly2 for capacitor spacing to unrelated metal >= 2')

print 'Checking poly2 for transistor rules...'
geomWidth(poly2_for_tran, 2*LAMBDA - EPSILON, '12.1 Poly2 for transistor width >= 2')
geomSpace(poly2_for_tran, 3*LAMBDA - EPSILON, 0, '12.2 Poly2 for transistor spacing >= 3')
geomNotch(poly2_for_tran, 3*LAMBDA - EPSILON, '12.2 Poly2 for transistor spacing >= 3')
geomExtension(poly2_for_tran, active, 2*LAMBDA - EPSILON, '12.3 Poly2 for transistor extension of active >= 2')
geomExtension(active, poly2_for_tran, 3*LAMBDA - EPSILON, '12.7 Active extension of poly2 for transistor >= 3')
geomSpace(poly2_for_tran, active, LAMBDA - EPSILON, 0, '12.4 Poly2 for transistor spacing to active >= 1')
geomOverlap(poly2_for_tran, poly, 2*LAMBDA - EPSILON, '12.5 Poly2 for transistor spacing or overlap of poly >= 2')
geomSpace(poly2_for_tran, geomOutside(poly2_for_tran, poly), 2*LAMBDA - EPSILON, 0, '12.5 Poly2 for transistor spacing or overlap of poly >= 2')
geomSpace(poly2_for_tran, polycon, 3*LAMBDA - EPSILON, 0, '12.6 Poly2 for transistor spacing to poly or active contact >= 3')
geomSpace(poly2_for_tran, activecon, 3*LAMBDA - EPSILON, 0, '12.6 Poly2 for transistor spacing to poly or active contact >= 3')

print 'Checking poly2 contact rules...'
geomArea(poly2con, (2*LAMBDA - EPSILON)**2, (2*LAMBDA + EPSILON)**2, '13.1 Exact poly2 contact size = 2 x 2')
geomWidth(poly2con, 2*LAMBDA - EPSILON, '13.1 Exact poly2 contact size = 2 x 2')
geomSpace(poly2con, 3*LAMBDA - EPSILON, 0, '13.2 Poly2 contact spacing >= 3')
geomEnclose(poly2_for_cap, poly2con_on_cap, 3*LAMBDA - EPSILON, '13.3 Poly2 for capacitor overlap of poly2 contact (on capacitor) >= 3')
geomEnclose(poly2, poly2con, 2*LAMBDA - EPSILON, '13.4 Poly2 overlap of poly2 contact (not on capacitor) >= 2')
geomSpace(poly2con, poly, 3*LAMBDA - EPSILON, 0, '13.5 Poly2 contact spacing to poly or active >= 3')
geomSpace(poly2con, active, 3*LAMBDA - EPSILON, 0, '13.5 Poly2 contact spacing to poly or active >= 3')

print 'Checking highres rules...'
geomWidth(hires, 4*LAMBDA - EPSILON, '27.1 Hires width >= 4')
geomSpace(hires, 4*LAMBDA - EPSILON, 0, '27.2 Hires spacing >= 4')
geomNotch(hires, 4*LAMBDA - EPSILON, '27.2 Hires spaceing >= 4')
geomSpace(hires, allcon, 2*LAMBDA - EPSILON, 0, '27.3 Hires to contact spacing >= 2 (no contacts allowed inside hires)')
saveDerived(geomAnd(hires, allcon), '27.3 Hires to contact spacing >= 2 (no contacts allowed inside hires)')
geomSpace(hires, active, 2*LAMBDA - EPSILON, 0, '27.4 Hires to external active spacing >= 2')
geomSpace(hires, geomAvoiding(hires, poly2), 2*LAMBDA - EPSILON, 0, '27.5 Hires spacing to external poly2 >= 2')
saveDerived(geomAnd(hires, nwell), '27.6 Resistor is poly2 inside hires; poly2 ends stick out for contacts, the entire resistor must be outside well and over field')
saveDerived(geomAnd(hires, active), '27.6 Resistor is poly2 inside hires; poly2 ends stick out for contacts, the entire resistor must be outside well and over field')
geomWidth(poly2_for_res, 5*LAMBDA - EPSILON, '27.7 Poly2 width in resistor >= 5')
geomSpace(poly2_for_res, 7*LAMBDA - EPSILON, 0, '27.8 Spacing of poly2 resistors >= 7 (in a single hires region)')
geomNotch(poly2_for_res, 7*LAMBDA - EPSILON, '27.8 Spacing of poly2 resistors >= 7 (in a single hires region)')
geomOverlap(poly2, hires, 2*LAMBDA - EPSILON, '27.9 Hires overlap of poly2 >= 2')

print 'Checking poly contact rules...'
geomArea(polycon, (2*LAMBDA - EPSILON)**2, (2*LAMBDA + EPSILON)**2, '5.1 Exact poly contact size = 2 x 2')
geomWidth(polycon, 2*LAMBDA - EPSILON, '5.1 Exact poly contact size = 2 x 2')
geomEnclose(poly, polycon, 1.5*LAMBDA - EPSILON, '5.2 Poly overlap of poly contact >= 1.5')
geomSpace(polycon, 3*LAMBDA - EPSILON, 0, '5.3 Poly contact spacing >= 3')
geomSpace(polycon, gate, 2*LAMBDA - EPSILON, 0, '5.4 Poly contact spacing to gate of transistor >= 2')

print 'Checking active contact rules...'
geomArea(activecon, (2*LAMBDA - EPSILON)**2, (2*LAMBDA + EPSILON)**2, '6.1 Exact active contact size = 2 x 2')
geomWidth(activecon, 2*LAMBDA - EPSILON, '6.1 Exact active contact size = 2 x 2')
geomEnclose(active, activecon, 1.5*LAMBDA - EPSILON, '6.2 Active overlap of active contact >= 1.5')
geomSpace(activecon, 3*LAMBDA - EPSILON, 0, '6.3 Active contact spacing >= 3')
geomSpace(activecon, gate, 2*LAMBDA - EPSILON, 0, '6.4 Active contact spacing to gate of transistor >= 2')

print 'Checking metal1 rules...'
geomWidth(metal1, 3*LAMBDA - EPSILON, '7.1 Metal1 width >= 3')
geomSpace(metal1, 3*LAMBDA - EPSILON, 0, '7.2 Metal1 spacing >= 3')
geomEnclose(metal1, allcon, LAMBDA - EPSILON, '7.3 Metal1 overlap of any contact >= 1')
wide_metal1 = geomSize(geomSize(metal1, -5*LAMBDA), 5*LAMBDA)
narrow_m1_not_touching_wide_m1 = geomAvoiding(wide_metal1, metal1)
#narrow_metal1 = geomAndNot(metal1, wide_metal1)
#narrow_m1_touching_wide_m1 = geomTouching(wide_metal1, narrow_metal1)
#narrow_m1_not_touching_wide_m1 = geomAndNot(narrow_metal1, narrow_m1_touching_wide_m1)
geomSpace(wide_metal1, 6*LAMBDA - EPSILON, 0, '7.4 Metal1 spacing when either metal line is wider than 10 >= 6')
geomSpace(wide_metal1, narrow_m1_not_touching_wide_m1, 6*LAMBDA - EPSILON, 0, '7.4 Metal1 spacing when either metal line is wider than 10 >= 6')
#geomSpace(metal1, 6*LAMBDA, 10*LAMBDA, 0, '7.4 Metal1 spacing when either metal line is wider rthan 10 >= 6')

print 'Checking via rules...'
geomArea(via, (2*LAMBDA - EPSILON)**2, (2*LAMBDA + EPSILON)**2, '8.1 Exact via size = 2 x 2')
geomWidth(via, 2*LAMBDA - EPSILON, '8.1 Exact via size = 2 x 2')
geomSpace(via, 3*LAMBDA - EPSILON, 0, '8.2 Via spacing >= 3')
geomEnclose(metal1, via, LAMBDA - EPSILON, '8.3 Metal1 overlap of via >= 1')

print 'Checking metal2 rules...'
geomWidth(metal2, 3*LAMBDA - EPSILON, '9.1 Metal2 width >= 3')
geomSpace(metal2, 3*LAMBDA - EPSILON, 0, '9.2 Metal2 spacing >= 3')
geomEnclose(metal2, via, LAMBDA - EPSILON, '9.3 Metal2 overlap of via >= 1')
wide_metal2 = geomSize(geomSize(metal2, -5*LAMBDA), 5*LAMBDA)
narrow_m2_not_touching_wide_m2 = geomAvoiding(wide_metal2, metal2)
#narrow_metal2 = geomAndNot(metal2, wide_metal2)
#narrow_m2_touching_wide_m2 = geomTouching(wide_metal2, narrow_metal2)
#narrow_m2_not_touching_wide_m2 = geomAndNot(narrow_metal2, narrow_m2_touching_wide_m2)
geomSpace(wide_metal2, 6*LAMBDA - EPSILON, 0, '9.4 Metal2 spacing when either metal line is wider than 10 >= 6')
geomSpace(wide_metal2, narrow_m2_not_touching_wide_m2, 6*LAMBDA - EPSILON, 0, '9.4 Metal2 spacing when either metal line is wider than 10 >= 6')
#geomSpace(metal2, 6*LAMBDA, 10*LAMBDA, 0, '9.4 Metal2 spacing when either metal line is wider rthan 10 >= 6')

print 'Checking via2 rules...'
geomArea(via2, (2*LAMBDA - EPSILON)**2, (2*LAMBDA + EPSILON)**2, '14.1 Exact via2 size = 2 x 2')
geomWidth(via2, 2*LAMBDA - EPSILON, '14.1 Exact via2 size = 2 x 2')
geomSpace(via2, 3*LAMBDA - EPSILON, 0, '14.2 Via2 spacing >= 3')
geomEnclose(metal2, via2, LAMBDA - EPSILON, '14.3 Metal2 overlap of via2 >= 1')

print 'Checking metal3 rules...'
geomWidth(metal3, 5*LAMBDA - EPSILON, '15.1 Metal3 width >= 5')
geomSpace(metal3, 3*LAMBDA - EPSILON, 0, '15.2 Metal3 spacing >= 3')
geomEnclose(metal3, via2, 2*LAMBDA - EPSILON, '15.3 Metal3 overlap of via2 >= 2')
wide_metal3 = geomSize(geomSize(metal3, -5*LAMBDA), 5*LAMBDA)
narrow_m3_not_touching_wide_m3 = geomAvoiding(wide_metal3, metal3)
#narrow_metal3 = geomAndNot(metal3, wide_metal3)
#narrow_m3_touching_wide_m3 = geomTouching(wide_metal3, narrow_metal3)
#narrow_m3_not_touching_wide_m3 = geomAndNot(narrow_metal3, narrow_m3_touching_wide_m3)
geomSpace(wide_metal3, 6*LAMBDA - EPSILON, 0, '15.4 Metal3 spacing when either metal line is wider than 10 >= 6')
geomSpace(wide_metal3, narrow_m3_not_touching_wide_m3, 6*LAMBDA - EPSILON, 0, '15.4 Metal3 spacing when either metal line is wider than 10 >= 6')
#geomSpace(metal3, 6*LAMBDA, 10*LAMBDA, 0, '15.4 Metal3 spacing when either metal line is wider rthan 10 >= 6')

print 'Checking overglass rules...'
geomWidth(bonding_passivation, 60. - EPSILON, '10.1 Bonding passivation opening >= 60um')
geomWidth(probe_passivation, 20. - EPSILON, '10.2 Probe passivation opening >= 20um')
geomEnclose(metal3, glass, 6. - EPSILON, '10.3 Pad metal overlap of passivation >= 6um')
#geomSpace(pad_metal, metal3, 30. - EPSILON, diffnet, '10.4 Pad spacing to unrelated metal3 >= 30um')
#geomSpace(pad_metal, metal2, 15. - EPSILON, diffnet, '10.5a Pad spacing to unrelated metal2 >= 15um')
#geomSpace(pad_metal, metal1, 15. - EPSILON, diffnet, '10.5a Pad spacing to unrelated metal1 >= 15um')
geomSpace(pad_metal, active, 15. - EPSILON, 0, '10.5 Pad spacing to active, poly, or poly2 >= 15um')
geomSpace(pad_metal, poly, 15. - EPSILON, 0, '10.5 Pad spacing to active, poly, or poly2 >= 15um')
geomSpace(pad_metal, poly2, 15. - EPSILON, 0, '10.5 Pad spacing to active, poly, or poly2 >= 15um')

num_errors = geomGetTotalCount()
if num_errors==0:
    print 'No DRC errors were found.'
else:
    print 'Found {0!s} DRC error{1}.'.format(num_errors, 's' if num_errors>1 else '')

# Exit DRC package, freeing memory.
geomEnd()

ui().winRedraw()
