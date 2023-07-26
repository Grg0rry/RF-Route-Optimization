import os, sys
from matplotlib import pyplot as plt

sys.path.append('models/')
import environment
import agent
import dijkstra


def sumo_configuration():
    os.environ["SUMO_HOME"] = "D:/app/SUMO/SUMO/" # -- change to own directory

    # Check if SUMO sucessfully configured
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")


if __name__ == '__main__':
    # 01 Setup SUMO
    sumo_configuration()


    # 02 Configure network variables
    # -------------------
    # 2x3 Traffic Network
    # [A, B, C, D, E, F, G, H, I, J, K, L, M, N]
    # -------------------
    network_file = './network_files/2x3_network.net.xml'
    congestion = [("gneF_I", 10), ("gneI_F", 10), ("gneB_E", 20), ("gneE_B", 20), ("gneJ_M", 30), ("gneM_J", 30)]
    traffic_light = [("B", 5), ("I", 5), ("G", 5)]
    start_node = "A"
    end_node = "N"

    # -------------------
    # Sunway City Traffic Network
    # [101: Sunway University, 102: Monash University, 103: Sunway Geo, 104: Sunway Medical, 105: Taylors University, 106: Sunway Pyramid, 107: Sunway Lagoon, 108: PJS10 Park]
    # -------------------
    network_file = './network_files/sunway_network.net.xml'
    congestion = [("gne2124969573_1000000001", 10), ("gne677583745_2302498575", 10), ("gne5236931684_143675326", 20), ("gne1000000001_5735834058", 20), ("gne10734244602_1640449323", 10)]
    traffic_light = [(["2124969573", "2124969571"], 5), (["677583896", "1670458823"], 5), (["2210133573", "2210133562", "2210133501", "2210133223"], 5), (["4123498067", "4123498068", "2210132568", "2210132847"], 5), (["1197884608", "1197880914", "1197884584", "269953766"], 5), (["5762726921", "8948947765", "10845806303", "10845816012"], 5), (["677583804", "677583801", "677583803", "677583802"], 5), (["7211376203", "7211376202", "7211376200", "7211376201"], 5), (["2747527085", "1636307448", "678457498", "5780613945", "5780613944"], 5), (["5727497437", "5727497436", "678457587", "678457535"], 5), (["463099148", "1197913517"], 5), ("712814465", 5), ("1197913486", 5), ("9209244285", 5)]
    start_node = "101"
    end_node = "105"

    # -- Low traffic density
    # congestion = [('gne7248352139_1197884603', 20), ('gne1197879649_1197879633', 14), ('gne1197874335_1197874356', 20), ('gne2302498307_2302498392', 20), ('gne2210030932_2210030940', 11), ('gne2204295706_2204295552', 19), ('gne1197884606_1197884598', 20), ('gne1197879637_8632184543', 12), ('gne678457352_678457366', 18), ('gne1197874473_1197874414', 13), ('gne678457801_678457800', 12), ('gne677583771_677583772', 17), ('gne1197874356_1197874428', 16), ('gne1197874349_1197874386', 14), ('gne1197879623_1197879660', 20), ('gne2124969573_2124969571', 18), ('gne2210030056_2210030374', 13), ('gne677618955_2210029776', 20), ('gne678458018_280459116', 15), ('gne1197874337_7222893122', 10), ('gne678457402_678457371', 13), ('gne1640450753_4921551158', 10), ('gne8632184545_8632184679', 15), ('gne677583769_677583762', 16), ('gne2204295265_2204295275', 14), ('gne677583796_677583797', 11), ('gne678457800_678457801', 13), ('gne2302498389_2302498359', 19), ('gne106_10734244602', 15), ('gne1197888442_1197888420', 13), ('gne677583771_677583800', 20), ('gne4300141715_4300141717', 17), ('gne1197888437_1197888425', 16), ('gne2124949151_2124949155', 20), ('gne4123498096_2210031191', 17), ('gne1197874495_1197874385', 12), ('gne5735834068_1197884604', 14), ('gne1197879630_1197879644', 12), ('gne5236931696_5236931695', 13), ('gne4729109994_1197913467', 18), ('gne678458038_280459824', 18), ('gne2210133562_2210133501', 14), ('gne1197874386_1197874349', 19), ('gne677583818_677583814', 16), ('gne678457324_678457269', 19), ('gne1197880917_1197884583', 16), ('gne5735834064_1000000002', 15), ('gne1197874460_1197874388', 13), ('gne678457361_678457402', 12), ('gne269953946_143675841', 18), ('gne7222893125_7222893123', 17), ('gne712814477_1197892771', 11), ('gne5236932237_5236931692', 10), ('gne678457517_678457537', 11), ('gne143676093_143675841', 12), ('gne1197874435_1197874461', 20), ('gne1197874387_1197874435', 12), ('gne2210029837_2210030002', 20), ('gne269953829_143675842', 16), ('gne1197874460_1197874485', 19), ('gne1197879636_1197879651', 11), ('gne677583802_677583801', 16), ('gne7246269656_9122427638', 16), ('gne5472416434_5472416435', 19), ('gne1197892756_1197892767', 17), ('gne5727497444_5727497443', 18), ('gne5236931684_143675326', 14), ('gne1670458830_1670458788', 18)]
    # -- Medium traffic density
    # congestion = [('gne7248352139_1197884603', 14), ('gne1197879649_1197879633', 18), ('gne1197874335_1197874356', 12), ('gne2302498307_2302498392', 18), ('gne2210030932_2210030940', 11), ('gne2204295706_2204295552', 20), ('gne1197884606_1197884598', 14), ('gne1197879637_8632184543', 20), ('gne678457352_678457366', 18), ('gne1197874473_1197874414', 19), ('gne678457801_678457800', 13), ('gne677583771_677583772', 12), ('gne1197874356_1197874428', 15), ('gne1197874349_1197874386', 12), ('gne1197879623_1197879660', 18), ('gne2124969573_2124969571', 18), ('gne2210030056_2210030374', 10), ('gne677618955_2210029776', 19), ('gne678458018_280459116', 15), ('gne1197874337_7222893122', 17), ('gne678457402_678457371', 10), ('gne1640450753_4921551158', 11), ('gne8632184545_8632184679', 15), ('gne677583769_677583762', 14), ('gne2204295265_2204295275', 13), ('gne677583796_677583797', 10), ('gne678457800_678457801', 13), ('gne2302498389_2302498359', 19), ('gne106_10734244602', 11), ('gne1197888442_1197888420', 11), ('gne677583771_677583800', 17), ('gne4300141715_4300141717', 11), ('gne1197888437_1197888425', 18), ('gne2124949151_2124949155', 12), ('gne4123498096_2210031191', 12), ('gne1197874495_1197874385', 20), ('gne5735834068_1197884604', 17), ('gne1197879630_1197879644', 18), ('gne5236931696_5236931695', 12), ('gne4729109994_1197913467', 14), ('gne678458038_280459824', 18), ('gne2210133562_2210133501', 19), ('gne1197874386_1197874349', 16), ('gne677583818_677583814', 13), ('gne678457324_678457269', 18), ('gne1197880917_1197884583', 13), ('gne5735834064_1000000002', 14), ('gne1197874460_1197874388', 16), ('gne678457361_678457402', 20), ('gne269953946_143675841', 20), ('gne7222893125_7222893123', 15), ('gne712814477_1197892771', 17), ('gne5236932237_5236931692', 18), ('gne678457517_678457537', 17), ('gne143676093_143675841', 11), ('gne1197874435_1197874461', 13), ('gne1197874387_1197874435', 13), ('gne2210029837_2210030002', 11), ('gne269953829_143675842', 15), ('gne1197874460_1197874485', 10), ('gne1197879636_1197879651', 19), ('gne677583802_677583801', 18), ('gne7246269656_9122427638', 13), ('gne5472416434_5472416435', 19), ('gne1197892756_1197892767', 13), ('gne5727497444_5727497443', 10), ('gne5236931684_143675326', 11), ('gne1670458830_1670458788', 20), ('gne2210826388_2210826253', 10), ('gne8632184543_8632184677', 13), ('gne1197874442_1197874387', 11), ('gne678458063_280458836', 10), ('gne7246269656_1197913486', 15), ('gne1197892781_4729109994', 11), ('gne678457279_678457274', 18), ('gne1197892756_712814477', 13), ('gne677583826_2210826868', 14), ('gne5735834064_677583803', 20), ('gne2210826767_2210826253', 17), ('gne7248352139_5735834069', 13), ('gne678457370_678457375', 18), ('gne2204294872_2204295706', 12), ('gne280465223_678457994', 19), ('gne1197874402_1197874387', 19), ('gne2210029963_2210029752', 17), ('gne280460729_280462229', 13), ('gne5778793362_678457169', 17), ('gne2210826388_677583833', 16), ('gne1197874432_1197874358', 13), ('gne1694168120_269953829', 11), ('gne678457462_678457454', 11), ('gne280460729_1192884325', 20), ('gne1984009884_1984009870', 16), ('gne8759340685_8759340684', 15), ('gne677618895_2210031167', 16), ('gne5778792535_5732957384', 16), ('gne7993603231_7993603234', 17), ('gne677583814_677583819', 10), ('gne1197888419_1197888424', 20), ('gne2210133573_2210133562', 20), ('gne2210031167_2210030414', 20), ('gne678457341_678457339', 11), ('gne2210133494_7993603237', 10), ('gne678457796_678457797', 16), ('gne677583776_677583777', 15), ('gne678457796_678457364', 11), ('gne5778793223_678457273', 13), ('gne5236932237_5236932233', 13), ('gne1197884605_269953766', 13), ('gne678457166_678457164', 18), ('gne677618806_677618821', 17), ('gne1197874490_1197874397', 12), ('gne1197874388_1197874426', 16), ('gne1197879647_1197879644', 12), ('gne1197888435_1197888420', 14), ('gne7222893122_660840279', 17), ('gne1197888445_1197888437', 13), ('gne678458000_678457279', 11), ('gne1197874427_1197874467', 17), ('gne5762708414_5762708412', 18), ('gne5735834073_2000878251', 11), ('gne678458000_678457193', 10), ('gne677583853_677583887', 20), ('gne678457260_678457269', 18), ('gne2210031289_2210029755', 10), ('gne678457364_678457363', 11), ('gne10845816010_10845816005', 13), ('gne1197879652_1197879661', 12), ('gne678457339_280465223', 16), ('gne7682106896_1197879633', 17), ('gne269953946_1984009884', 17), ('gne677583780_677583790', 13), ('gne1197888440_1197888420', 16), ('gne677583803_5735834068', 10), ('gne10311852155_10311852158', 12)]    
    # -- High traffic density
    # congestion = [('gne7248352139_1197884603', 11), ('gne1197879649_1197879633', 19), ('gne1197874335_1197874356', 11), ('gne2302498307_2302498392', 20), ('gne2210030932_2210030940', 13), ('gne2204295706_2204295552', 16), ('gne1197884606_1197884598', 11), ('gne1197879637_8632184543', 19), ('gne678457352_678457366', 13), ('gne1197874473_1197874414', 19), ('gne678457801_678457800', 19), ('gne677583771_677583772', 10), ('gne1197874356_1197874428', 19), ('gne1197874349_1197874386', 11), ('gne1197879623_1197879660', 16), ('gne2124969573_2124969571', 20), ('gne2210030056_2210030374', 19), ('gne677618955_2210029776', 19), ('gne678458018_280459116', 18), ('gne1197874337_7222893122', 15), ('gne678457402_678457371', 14), ('gne1640450753_4921551158', 13), ('gne8632184545_8632184679', 20), ('gne677583769_677583762', 15), ('gne2204295265_2204295275', 13), ('gne677583796_677583797', 14), ('gne678457800_678457801', 16), ('gne2302498389_2302498359', 12), ('gne106_10734244602', 20), ('gne1197888442_1197888420', 20), ('gne677583771_677583800', 14), ('gne4300141715_4300141717', 17), ('gne1197888437_1197888425', 15), ('gne2124949151_2124949155', 11), ('gne4123498096_2210031191', 10), ('gne1197874495_1197874385', 17), ('gne5735834068_1197884604', 19), ('gne1197879630_1197879644', 19), ('gne5236931696_5236931695', 11), ('gne4729109994_1197913467', 11), ('gne678458038_280459824', 18), ('gne2210133562_2210133501', 13), ('gne1197874386_1197874349', 18), ('gne677583818_677583814', 14), ('gne678457324_678457269', 12), ('gne1197880917_1197884583', 15), ('gne5735834064_1000000002', 11), ('gne1197874460_1197874388', 13), ('gne678457361_678457402', 15), ('gne269953946_143675841', 14), ('gne7222893125_7222893123', 12), ('gne712814477_1197892771', 17), ('gne5236932237_5236931692', 18), ('gne678457517_678457537', 14), ('gne143676093_143675841', 19), ('gne1197874435_1197874461', 20), ('gne1197874387_1197874435', 18), ('gne2210029837_2210030002', 10), ('gne269953829_143675842', 20), ('gne1197874460_1197874485', 18), ('gne1197879636_1197879651', 14), ('gne677583802_677583801', 20), ('gne7246269656_9122427638', 11), ('gne5472416434_5472416435', 12), ('gne1197892756_1197892767', 14), ('gne5727497444_5727497443', 11), ('gne5236931684_143675326', 11), ('gne1670458830_1670458788', 18), ('gne2210826388_2210826253', 12), ('gne8632184543_8632184677', 14), ('gne1197874442_1197874387', 14), ('gne678458063_280458836', 19), ('gne7246269656_1197913486', 13), ('gne1197892781_4729109994', 15), ('gne678457279_678457274', 13), ('gne1197892756_712814477', 20), ('gne677583826_2210826868', 20), ('gne5735834064_677583803', 14), ('gne2210826767_2210826253', 18), ('gne7248352139_5735834069', 17), ('gne678457370_678457375', 14), ('gne2204294872_2204295706', 10), ('gne280465223_678457994', 11), ('gne1197874402_1197874387', 20), ('gne2210029963_2210029752', 16), ('gne280460729_280462229', 14), ('gne5778793362_678457169', 10), ('gne2210826388_677583833', 10), ('gne1197874432_1197874358', 15), ('gne1694168120_269953829', 12), ('gne678457462_678457454', 20), ('gne280460729_1192884325', 14), ('gne1984009884_1984009870', 12), ('gne8759340685_8759340684', 17), ('gne677618895_2210031167', 18), ('gne5778792535_5732957384', 16), ('gne7993603231_7993603234', 18), ('gne677583814_677583819', 10), ('gne1197888419_1197888424', 11), ('gne2210133573_2210133562', 11), ('gne2210031167_2210030414', 12), ('gne678457341_678457339', 18), ('gne2210133494_7993603237', 10), ('gne678457796_678457797', 15), ('gne677583776_677583777', 19), ('gne678457796_678457364', 18), ('gne5778793223_678457273', 12), ('gne5236932237_5236932233', 16), ('gne1197884605_269953766', 12), ('gne678457166_678457164', 10), ('gne677618806_677618821', 14), ('gne1197874490_1197874397', 15), ('gne1197874388_1197874426', 10), ('gne1197879647_1197879644', 15), ('gne1197888435_1197888420', 13), ('gne7222893122_660840279', 20), ('gne1197888445_1197888437', 13), ('gne678458000_678457279', 20), ('gne1197874427_1197874467', 11), ('gne5762708414_5762708412', 15), ('gne5735834073_2000878251', 18), ('gne678458000_678457193', 16), ('gne677583853_677583887', 19), ('gne678457260_678457269', 12), ('gne2210031289_2210029755', 13), ('gne678457364_678457363', 12), ('gne10845816010_10845816005', 12), ('gne1197879652_1197879661', 16), ('gne678457339_280465223', 10), ('gne7682106896_1197879633', 12), ('gne269953946_1984009884', 15), ('gne677583780_677583790', 16), ('gne1197888440_1197888420', 20), ('gne677583803_5735834068', 13), ('gne10311852155_10311852158', 14), ('gne2210133501_2210133223', 12), ('gne677618899_2210031167', 11), ('gne1197913474_4729110010', 16), ('gne677619034_677618890', 10), ('gne1197879642_1197879634', 17), ('gne7211376202_269953935', 13), ('gne2747527091_4921551158', 13), ('gne7248340682_7222893125', 17), ('gne5732957394_678457324', 15), ('gne1197888448_1197892782', 14), ('gne678457341_678457375', 13), ('gne678457269_678457324', 13), ('gne1000000001_5735834058', 10), ('gne678458014_678457222', 20), ('gne280465223_678457339', 13), ('gne677583895_677583856', 16), ('gne1186819607_1197874337', 15), ('gne1197879649_1197879659', 14), ('gne5281743138_1197892781', 11), ('gne2747527105_2747527100', 14), ('gne2210030753_2210031389', 15), ('gne1197874412_1197874403', 20), ('gne2210030796_2210030932', 18), ('gne1197874470_1197874490', 16), ('gne677583887_677583896', 20), ('gne1197874435_1197874387', 18), ('gne678457274_5778793223', 15), ('gne1197880926_1197880927', 10), ('gne1197884570_1197884584', 11), ('gne9354798730_2747527094', 14), ('gne677583872_677583870', 12), ('gne678457357_678457234', 19), ('gne1197892763_1197913456', 14), ('gne678457234_678458031', 10), ('gne678458054_280458836', 11), ('gne677583772_677583771', 19), ('gne1694168207_660840277', 16), ('gne1640452984_108', 15), ('gne280459824_5778792533', 15), ('gne5732957394_678457260', 16), ('gne677583783_677583760', 19), ('gne678457181_5778793364', 18), ('gne677583800_677583806', 11), ('gne1197879662_1197879649', 16), ('gne2210031167_677618899', 19), ('gne2210029752_2210029963', 13), ('gne1197874428_1197874347', 14), ('gne4123498120_4123498116', 10), ('gne1186819608_1197874444', 16), ('gne678457800_1640452980', 10), ('gne678457364_678457796', 18), ('gne2210030002_2210031246', 18), ('gne678457800_678457405', 20), ('gne10734244602_106', 20), ('gne1197874442_1186819607', 13), ('gne7243153330_5236932237', 15), ('gne1197874412_1197874452', 16), ('gne2210029963_1197884606', 11), ('gne1197874432_1197874444', 20), ('gne1197874356_1197874426', 15), ('gne2919814563_678457405', 19), ('gne678457171_678457273', 15), ('gne2210030384_2210030487', 20), ('gne2302498389_2302498384', 11), ('gne677583887_1670458757', 14), ('gne2000878251_677583780', 18), ('gne1197884584_269953766', 14), ('gne678457466_678457502', 20), ('gne678457505_678457502', 16), ('gne677583870_677583871', 15), ('gne2210030870_5762726905', 16), ('gne660840277_712814473', 14), ('gne143675841_1640449330', 18), ('gne1197879624_8004778229', 12), ('gne9209244285_5778223858', 13), ('gne677583777_677583779', 16), ('gne4921555285_2747527095', 20), ('gne677583772_677583773', 16), ('gne677583760_677583763', 20), ('gne677583853_1218366993', 12), ('gne1197874400_1197874353', 19), ('gne8634431542_678457357', 19), ('gne8004778229_1197879661', 14), ('gne1197879633_8004778229', 16), ('gne1197874420_1197874361', 18), ('gne5778793364_678457181', 10), ('gne4300141713_2204295265', 14), ('gne1197879647_1197879641', 14), ('gne2210031191_4123498088', 13), ('gne143675842_7211376202', 16), ('gne677583796_677583776', 19), ('gne1197884608_1197884584', 19), ('gne1197913494_1197913460', 20), ('gne677583826_677583822', 15), ('gne2210031253_2210030870', 17), ('gne1197874450_1197874369', 17), ('gne677583789_677583785', 17), ('gne678457360_678457361', 20), ('gne1197879633_7682106896', 13), ('gne1197874397_1197874490', 18), ('gne8632184679_1197879660', 17), ('gne678457343_678457370', 12), ('gne1186819601_1197879636', 20), ('gne2210030374_2210030056', 11), ('gne1197892763_1197913485', 14), ('gne660840277_712814466', 18), ('gne677583876_677583861', 20), ('gne2000878251_677583771', 20), ('gne1197892762_1197892782', 19), ('gne5735834064_5735834068', 15), ('gne101_2124969571', 11), ('gne5778246029_2968534235', 13), ('gne2210826253_2210826388', 20), ('gne677583804_5735834058', 14), ('gne2688164830_2747527094', 13), ('gne678457370_678457343', 13), ('gne677583892_1670458771', 12), ('gne1197888437_1197888419', 10), ('gne1218366993_677583853', 10), ('gne2747527090_7245815529', 13), ('gne2124969573_101', 17), ('gne1197874412_1197874432', 19), ('gne678457537_678457535', 11), ('gne678457344_678458014', 17), ('gne280460595_5762708412', 16), ('gne1197874403_1197874412', 20), ('gne1197874397_1197874473', 19), ('gne678457796_678457706', 13), ('gne677583873_677583872', 16), ('gne677618908_7248352139', 17), ('gne678457273_5778793223', 16), ('gne1197888438_1197888440', 13), ('gne1197874403_1197874400', 12), ('gne677619044_677618886', 20), ('gne1197874461_1197874386', 10), ('gne1197913508_4729110010', 11)]


    # 03 Initiate Environment
    env = environment.traffic_env(network_file, congestion, traffic_light, evaluation = "d")
    # env = environment.traffic_env(network_file = network_file, traffic_light = traffic_light, evaluation = "t", congestion_level = "low")
    num_episodes = 5000
    num_converge = 5


    # 04 Activate Agent
    # -------------------
    # Dijkstra Algorithm
    # -------------------
    print(f'Dijkstra Algorithm{"." * 100}')
    Dijkstra = dijkstra.Dijkstra(env, start_node, end_node)
    node_path, edge_path, *_ = Dijkstra.search()
    env.visualize_plot(edge_path)

    # -------------------
    # Q_Learning Algorithm
    # -------------------
    print(f'\nQ_Learning Algorithm{"." * 100}')
    Q_agent = agent.Q_Learning(env, start_node, end_node)
    node_path, edge_path, episode, logs = Q_agent.train(num_episodes, num_converge)
    env.plot_performance(episode, logs)
    env.visualize_plot(edge_path)

    # -------------------
    # SARSA Algorithm
    # -------------------
    print(f'\nSARSA Algorithm{"." * 100}')
    S_agent = agent.SARSA(env, start_node, end_node, exploration_rate = 0.1)
    node_path, edge_path, episode, logs = S_agent.train(num_episodes, num_converge)
    env.plot_performance(episode, logs)
    env.visualize_plot(edge_path)