import asg.cliche.Command;
import asg.cliche.ShellFactory;

import java.io.IOException;
import java.util.Scanner;


public class subnetting {
    private int first_oct = -1;
    private int second_oct = -1;
    private int third_oct = -1;
    private int fourth_oct = -1;
    private int slash_mask = -1;
    int[] binary_ip = {-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1};
    private int[] binary_mask = {-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1};
    private String decimal_ip = "Error: IP-Address wasn't specified !";
    private String decimal_mask = "Error: Subnet wasn't specified !";
    private String decimal_network_address = "Didn't calculate Ranges yet !";
    private String decimal_broadcast_address = "Didn't calculate Ranges yet !";

    private int[] decimal_Byte_To_Binary(int oct) {

        if (oct < 0 || oct > 255) {
            System.out.println("Error: oct wrong : " + oct);

            return new int[0];
        }
        int[] bioct = new int[8];
        for (int i = 0; i < 8; i++) {
            if (oct % 2 == 1) {
                bioct[7 - i] = 1;
                oct--;
            } else {
                bioct[7 - i] = 0;
            }
            oct = oct / 2;

        }


        return bioct;
    }

    private int binary_Byte_To_Decimal(int[] binary) {
        int oct = 0;
        if (binary.length != 8) {
            System.out.println("Error: binary array not 8 bits");

            return -1;
        }

        for (int i = 0; i < 8; i++) {
            if (binary[i] == 1) {
                oct += (int) Math.pow(2.0, (double) 7 - i);

            }
        }
        return oct;
    }

    private boolean is_Not_Valid_Oct(int oct) {
        if (oct < 256 && oct > -1) {
            return false;
        }

        return true;
    }

    @Command(name = "scan_Subnet_Mask_In_Slash", abbrev = "1")//one
    public void scan_Subnet_Mask_In_Slash() {
        Scanner myscan = new Scanner(System.in);
        String input = myscan.next();
        input = input.replace("/", "");
        if (!input.matches("\\d+")) {
            System.out.println("Error: wrong slash_mask: " + input);
            return;
        }
        slash_mask = Integer.parseInt(input);
        if (slash_mask < 0 || slash_mask > 30) {
            System.out.println("Error: wrong slash_mask: " + slash_mask);
            return;
        }
        for (int i = 0; i < 32; i++) {
            if (i < slash_mask) {
                binary_mask[i] = 1;
            } else {
                binary_mask[i] = 0;
            }
        }

        decimal_mask = convert_Binary_32_Bit_To_Decimal(binary_mask);


    }

    private boolean is_Full_IP_Address(String input) {
        String[] octett_ar;
        int[] octett_array = new int[4];
        octett_ar = input.split("\\.", 4);
        if (octett_ar.length != 4) {
            return false;
        }

        try {
            octett_array[0] = Integer.parseInt(octett_ar[0]);
        } catch (Exception e) {
            return false;
        }

        try {
            octett_array[1] = Integer.parseInt(octett_ar[1]);
        } catch (Exception e) {
            return false;
        }

        try {
            octett_array[2] = Integer.parseInt(octett_ar[2]);
        } catch (Exception e) {
            return false;
        }

        try {
            octett_array[3] = Integer.parseInt(octett_ar[3]);
        } catch (Exception e) {
            return false;
        }
        if (is_Not_Valid_Oct(octett_array[0])) {
            return false;
        }
        if (is_Not_Valid_Oct(octett_array[1])) {
            return false;
        }
        if (is_Not_Valid_Oct(octett_array[2])) {
            return false;
        }
        if (is_Not_Valid_Oct(octett_array[3])) {
            return false;
        }

        first_oct = octett_array[0];
        second_oct = octett_array[1];
        third_oct = octett_array[2];
        fourth_oct = octett_array[3];

        decimal_ip = (first_oct + "." + second_oct + "." + third_oct + "." + fourth_oct);
        copy_Decimal_IP_to_Binary_IP();
        print_Decimal_IP();
        return true;
    }

    @Command(name = "scan_Decimal_IP", abbrev = "2") //two
    public void scan_Decimal_IP() {
        Scanner myscan = new Scanner(System.in);
        String inputString;
        do {
            if (myscan.hasNextInt()) {
                first_oct = myscan.nextInt();
            } else {
                inputString = myscan.next().toLowerCase();
                //check if full ip address:
                if (is_Full_IP_Address(inputString)) {
                    return;
                }


                if (inputString.equals(("cancel")) || inputString.equals("c")) {
                    first_oct = -1;
                    return;
                }
                System.out.println("Please input only one Octet at a time !");
            }

        } while (is_Not_Valid_Oct(first_oct));

        do {
            System.out.print(first_oct + ".");
            if (myscan.hasNextInt()) {
                second_oct = myscan.nextInt();
            } else {
                inputString = myscan.next().toLowerCase();
                if (inputString.equals(("cancel")) || inputString.equals("c")) {
                    first_oct = -1;
                    second_oct = -1;
                    return;
                }
                System.out.println("Please input only one Octet at a time !");
            }
        } while (is_Not_Valid_Oct(second_oct));

        do {
            System.out.print(first_oct + "." + second_oct + ".");
            if (myscan.hasNextInt()) {
                third_oct = myscan.nextInt();
            } else {
                inputString = myscan.next().toLowerCase();
                if (inputString.equals(("cancel")) || inputString.equals("c")) {
                    first_oct = -1;
                    second_oct = -1;
                    third_oct = -1;
                    return;
                }
                System.out.println("Please input only one Octet at a time !");
            }
        } while (is_Not_Valid_Oct(third_oct));


        do {
            System.out.print(first_oct + "." + second_oct + "." + third_oct + ".");
            if (myscan.hasNextInt()) {
                fourth_oct = myscan.nextInt();
            } else {
                inputString = myscan.next().toLowerCase();
                if (inputString.equals(("cancel")) || inputString.equals("c")) {
                    first_oct = -1;
                    second_oct = -1;
                    third_oct = -1;
                    fourth_oct = -1;
                    return;
                }
                System.out.println("Please input only one Octet at a time !");
            }
        } while (is_Not_Valid_Oct(fourth_oct));
        decimal_ip = (first_oct + "." + second_oct + "." + third_oct + "." + fourth_oct);
        copy_Decimal_IP_to_Binary_IP();
        print_Decimal_IP();
    }

    @Command(name = "print_Decimal_IP", abbrev = "3") //three
    public void print_Decimal_IP() {
        System.out.println(decimal_ip);

    }


    private void copy_Decimal_IP_to_Binary_IP() {
        System.arraycopy(decimal_Byte_To_Binary(first_oct), 0, binary_ip, 0, 8);
        System.arraycopy(decimal_Byte_To_Binary(second_oct), 0, binary_ip, 8, 8);
        System.arraycopy(decimal_Byte_To_Binary(third_oct), 0, binary_ip, 16, 8);
        System.arraycopy(decimal_Byte_To_Binary(fourth_oct), 0, binary_ip, 24, 8);
    }

    @Command(name = "print_Binary_IP", abbrev = "4") //four
    public void print_Binary_IP() {
        if (binary_ip[0] == -1) {
            System.out.println("Error: IP-Address wasn't specified !");
            return;
        }
        for (int i = 0; i < 32; i++) {
            System.out.print(binary_ip[i]);
        }
        System.out.println();
    }

    @Command(name = "print_Binary_Mask", abbrev = "5") //five
    public void print_Binary_Mask() {
        if (binary_mask[0] == -1) {
            System.out.println("Error: Subnet wasn't specified !");
            return;
        }
        for (int i = 0; i < 32; i++) {
            System.out.print(binary_mask[i]);
        }
        System.out.println();
    }

    @Command(name = "print_Decimal_Mask", abbrev = "6") //six
    public void print_Decimal_Mask() {
        System.out.println(decimal_mask);

    }

    private String convert_Binary_32_Bit_To_Decimal(int[] origin) {
        String destination = "";
        int[] cur_bin = new int[8];
        int cur_int;

        System.arraycopy(origin, 0, cur_bin, 0, 8);
        cur_int = binary_Byte_To_Decimal(cur_bin);
        destination += (cur_int) + ".";
        System.arraycopy(origin, 8, cur_bin, 0, 8);
        cur_int = binary_Byte_To_Decimal(cur_bin);
        destination += (cur_int) + ".";
        System.arraycopy(origin, 16, cur_bin, 0, 8);
        cur_int = binary_Byte_To_Decimal(cur_bin);
        destination += (cur_int) + ".";
        System.arraycopy(origin, 24, cur_bin, 0, 8);
        cur_int = binary_Byte_To_Decimal(cur_bin);
        destination += (cur_int);
        return destination;
    }

    @Command(name = "show_Menu", abbrev = "7")//seven
    public void show_Menu() {

        System.out.println("What do you want to do ?");
        System.out.println(" 1:   scan_Subnet_Mask_In_Slash()");
        System.out.println(" 2:   scan_Decimal_IP()");
        System.out.println(" 3:   print_Decimal_IP()");
        System.out.println(" 4:   print_Binary_IP()");
        System.out.println(" 5:   print_Binary_Mask()");
        System.out.println(" 6:   print_Decimal_Mask()");
        System.out.println(" 7:   show_Menu()");
        System.out.println(" 8:   print_Number_Of_Possible_Hosts()");
        System.out.println(" 9:   calculate_Ranges()");
        System.out.println(" 10:  print_Network_Address()");
        System.out.println(" 11:  print_Broadcast_Address()");


    }

    @Command(name = "print_Number_Of_Possible_Hosts", abbrev = "8")//eight
    public void print_Number_Of_Possible_Hosts() {
        if (slash_mask != -1) {
            System.out.printf("%.0f\n", (Math.pow(2.0, (double) 32 - slash_mask) - 2));
        } else {
            System.out.println("Error: Subnet wasn't specified !");
        }

    }

    @Command(name = "calculate_Ranges", abbrev = "9") //nine
    public void calculate_Ranges() {
        if (slash_mask == -1) {
            if (decimal_ip.equals("Error: IP-Address wasn't specified !")) {
                System.out.println("Error: Subnet and IP-Address weren't specified !");
            }else {
                System.out.println("Error: Subnet wasn't specified !");
            }
            return;
        }
            if (decimal_ip.equals("Error: IP-Address wasn't specified !")) {
                System.out.println("Error: IP-Address wasn't specified !");

                return;
            }

        //network address
        int[] poly_address = binary_ip;
        for (int i = slash_mask; i < 32; i++) {
            poly_address[i] = 0;
        }

        decimal_network_address = convert_Binary_32_Bit_To_Decimal(poly_address);
        //broadcast address
        poly_address = binary_ip;
        for (int i = slash_mask; i < 32; i++) {
            poly_address[i] = 1;
        }
        decimal_broadcast_address = convert_Binary_32_Bit_To_Decimal(poly_address);
    }

    @Command(name = "print_Network_Address", abbrev = "10")//ten
    public void print_Network_Address() {
        System.out.println(decimal_network_address);

    }

    @Command(name = "print_Broadcast_Address", abbrev = "11") //eleven
    public void print_Broadcast_Address() {
        System.out.println(decimal_broadcast_address);

    }


    public static void main(String[] args) throws IOException {
        ShellFactory.createConsoleShell("7", "", new subnetting())
                .commandLoop();


    }
}