
class subnetter:
    def __init__(self):
        self.ipadress = ""
        self.subnetmask_in_slash = -1
        self.bin_ipadress = ""
        self.bin_subnetmask = ""

    def is_ready(self):
        bad = False
        if self.ipadress == "":
            bad = True
            print("no ipadress specified")
        if self.subnetmask_in_slash == -1:
            print("no subnetmask specified")
            bad = True
        if not bad:
            return True
        return False

    def check_if_binary_addres_is_valid(self, adress: str):
        if len(adress) != 32:
            return False
        for b in adress:
            if b not in ("0", "1"):
                return False
        return True

    def check_if_decimal_adress_is_valid(self, adress: str):
        loo = adress.split(".")
        if len(loo) != 4:
            return False
        for o in loo:
            if not o.isdigit():
                return False
            n = int(o)
            if n not in range(0, 256):
                return False
        return True

    def set_subnetmask_in_slash(self, mask: int):
        if type(mask) is str:
            numb = mask.replace("/", "")
            if not numb.isdigit():
                print("bad subnetmask")
                return
            mask = int(numb)
        if mask not in range(32):  # allows for 0 - 31 as subnetmasks
            print("bad subnetmask")
            return
        self.subnetmask_in_slash = mask
        a = ["1" if mask > i else "0" for i in range(32)]
        self.bin_subnetmask = ''.join(a)

    def set_subnetmask_in_binary(self, mask: str):
        if not self.check_if_binary_addres_is_valid(mask):
            print("bad subnetmask")
            return
        slash_mask = 0

        for i in range(32):
            if mask[i] == "1":
                slash_mask += 1
            else:
                for j in range(i, 32):
                    if mask[j] != "0":
                        print("bad subnetmask")
                        return
                break
        self.set_subnetmask_in_slash(slash_mask)

    def set_subnetmask_in_decimal(self, mask: str):
        bin_mask = self.decimal_adress_to_binary(mask)
        if bin_mask is None:
            print("bad subnetmask")
            return
        self.set_subnetmask_in_binary(bin_mask)

    def set_ipadress_in_decimal(self, adress: str):
        ret = self.decimal_adress_to_binary(adress)
        if ret is None:
            print("bad_ipadress")
            return
        self.ipadress = adress
        self.bin_ipadress = ret

    def set_ipadress_in_binary(self, adress: str):
        if not self.check_if_binary_addres_is_valid(adress):
            print("bad ipadress")
            return
        self.set_ipadress_in_decimal(self.binary_adress_to_decimal(adress))

    def show_dec_subnetmask(self):
        if self.subnetmask_in_slash == -1:
            print("no subnetmask specified")
            return
        print(self.binary_adress_to_decimal(self.bin_subnetmask))

    def show_bin_subnetmask(self):
        if self.subnetmask_in_slash == -1:
            print("no subnetmask specified")
            return
        print(self.bin_subnetmask)

    def show_slash_subnetmask(self):
        if self.subnetmask_in_slash == -1:
            print("no subnetmask specified")
            return
        print("/{}".format(self.subnetmask_in_slash))

    def show_dec_ipadress(self):
        if self.ipadress == "":
            print("no ipadress specified")
            return
        print(self.ipadress)

    def show_bin_ipadress(self):
        if self.bin_ipadress == "":
            print("no ipadress specified")
            return
        print(self.bin_ipadress)

    def show_number_of_hosts(self):
        if self.subnetmask_in_slash == -1:
            print("no subnetmask specified")
            return
        print(2**(32-self.subnetmask_in_slash)-2)

    def binary_adress_to_decimal(self, b_ip: str):
        while len(b_ip) < 32:
            b_ip = "0" + b_ip
        if not self.check_if_binary_addres_is_valid(b_ip):
            return
        loo = []
        for i in range(0, 32, 8):
            oct = b_ip[i:i+8]
            loo.append(str(int(oct, 2)))
        return '.'.join(loo)

    def decimal_adress_to_binary(self, adress):
        if not self.check_if_decimal_adress_is_valid(adress):
            return
        loo = adress.split(".")
        bin_ipadress = ""
        for o in loo:
            b_number = bin(int(o))[2:]
            while len(b_number) < 8:
                b_number = "0" + b_number
            bin_ipadress += b_number
        return bin_ipadress

    def show_host_ip_range(self):
        if not self.is_ready():
            return
        lob = list(self.bin_ipadress)
        for i in range(self.subnetmask_in_slash, 32):
            lob[i] = "0"
        # removes network address as an option
        bin_ip = bin(int("".join(lob), 2)+1)[2:]
        start_ip = self.binary_adress_to_decimal(bin_ip)
        for i in range(self.subnetmask_in_slash, 32):
            lob[i] = "1"
        # removes broadcast address as an option
        bin_ip = bin(int("".join(lob), 2)-1)[2:]
        end_ip = self.binary_adress_to_decimal(bin_ip)
        print(start_ip + " - " + end_ip)

    def show_network_adress(self):
        if not self.is_ready():
            return
        lob = list(self.bin_ipadress)
        for i in range(self.subnetmask_in_slash, 32):
            lob[i] = "0"
        print(self.binary_adress_to_decimal("".join(lob)))

    def show_broadcast_adress(self):
        if not self.is_ready():
            return
        lob = list(self.bin_ipadress)
        for i in range(self.subnetmask_in_slash, 32):
            lob[i] = "1"
        print(self.binary_adress_to_decimal("".join(lob)))


if __name__ == "__main__":
    s = subnetter()
    s.set_ipadress_in_decimal("2.172.21.252")
    # s.set_subnetmask(23)
    s.set_subnetmask_in_slash("/23")
    # s.show_subnetmask()
    # s.show_bin_subnetmask()
    # s.show_ipadress()
    # s.show_bin_ipadress()
    # s.show_number_of_hosts()
    s.show_host_ip_range()
    # s.show_network_adress()
    # s.show_broadcast_adress()
