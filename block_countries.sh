# Countries I could realistic see my self comming this is not intended as an oppion on the countries listed here.
# This is just to block traffic that could not possible be comming from people I personally know or know that servers
# Are located there that I need so just for safety we disable connections to a lot of the countries.

for code in DZ AO BJ BW BF BI CM CV CF TD KM CD DJ EG GQ ER SZ ET GA GM GH GN GW CI KE LS LR LY MG MW ML MR MU MA MZ NA NE NG CG RE RW ST SN SC SL SO ZA SS SD TZ TG TN UG EH ZM ZW
do
    iptables -A INPUT -m geoip --src-cc $code -j DROP
    iptables -A OUTPUT -m geoip --dst-cc $code -j DROP
done

for code in AR BO BR CL CO EC FK GF GY PE PY SR UY VE
do
    iptables -A INPUT -m geoip --src-cc $code -j DROP
    iptables -A OUTPUT -m geoip --dst-cc $code -j DROP
done

for code in AG BS BB CU DM DO GD HT JM KN LC VC TT
do
    iptables -A INPUT -m geoip --src-cc $code -j DROP
    iptables -A OUTPUT -m geoip --dst-cc $code -j DROP
done

for code in BY BG CZ HU MD PL RO RU SK UA
do
    iptables -A INPUT -m geoip --src-cc $code -j DROP
    iptables -A OUTPUT -m geoip --dst-cc $code -j DROP
done

for code in BH IR IQ IL JO KW LB OM QA SA SY AE YE TR
do
    iptables -A INPUT -m geoip --src-cc $code -j DROP
    iptables -A OUTPUT -m geoip --dst-cc $code -j DROP
done

for code in AF AZ BD BH BN BT CC CN CX CY GE HK ID IN IO IR JO JP KG KH KP KR KZ LA LB LK MM MN MO MV MY NP OM PH PK PS RU SA SG SY TH TJ TL TM TR TW UZ VN YE
do
    if [ "$code" != "JP" ] && [ "$code" != "KR" ] && [ "$code" != "TW" ]; then
        iptables -A INPUT -m geoip --src-cc $code -j DROP
        iptables -A OUTPUT -m geoip --dst-cc $code -j DROP
    fi
done

for code in BZ CR SV GT HN MX NI PA
do
    iptables -A INPUT -m geoip --src-cc $code -j DROP
    iptables -A OUTPUT -m geoip --dst-cc $code -j DROP
done

for code in AS AU CK FJ GU KI MH FM NR NC NZ NU NF MP PW PG PN WS SB TK TO TV UM VU WF
do
    if [ "$code" != "AU" ] && [ "$code" != "NZ" ]; then
        iptables -A INPUT -m geoip --src-cc $code -j DROP
        iptables -A OUTPUT -m geoip --dst-cc $code -j DROP
    fi
done

# Permanent
sudo iptables-save > /tmp/841402481084.txt
sudo mv /etc/iptables/rules.v4 /etc/iptables/rules.v4.backup
mv /tmp/841402481084.txt /etc/iptables/rules.v4