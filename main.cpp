#include "hwlib.hpp"

extern "C" int print_char(int c){
    return c;							///return the character, so that r0 wont be changed
}

extern "C" int fillListWithCheese(int * lijst, int length);

extern "C" int sommig(int n);

extern "C" int even(int n);

extern "C" int odd(int n);

extern "C" int getCheese(int * lijst, int length, int n);

int testeven(){
    int count = 0;
    int result = 0;
    hwlib::cout << "Testing even with 0"<< hwlib::endl;
    hwlib::cout << "Result = ";
    result = int(even(0));
    hwlib::cout << result;
    hwlib::cout << " : Should be 1\n";
    hwlib::cout << hwlib::endl;
    if (result == 1){
        count += 1;
    }

    hwlib::cout << "Testing even with 9"<< hwlib::endl;
    hwlib::cout << "Result = ";
    result = int(even(9));
    hwlib::cout << result;
    hwlib::cout << " : Should be 0\n";
    hwlib::cout << hwlib::endl;
    if (result == 0){
        count += 1;
    }


    hwlib::cout << "Testing even with 8"<< hwlib::endl;
    hwlib::cout << "Result = ";
    result = int(even(8));
    hwlib::cout << result;
    hwlib::cout << " : Should be 1\n";
    hwlib::cout << hwlib::endl;
    if (result == 1){
        count += 1;
    }


    hwlib::cout << "Testing even with -9"<< hwlib::endl;
    hwlib::cout << "Result = ";
    result = int(even(-9));
    hwlib::cout << result;
    hwlib::cout << " : Should be 0\n";
    hwlib::cout << hwlib::endl;
    if (result == 0){
        count += 1;
    }


    hwlib::cout << "Testing even with -8"<< hwlib::endl;
    hwlib::cout << "Result = ";
    result = int(even(-8));
    hwlib::cout << result;
    hwlib::cout << " : Should be 1\n";
    hwlib::cout << hwlib::endl;
    if (result == 1){
        count += 1;
    }

    hwlib::cout << "Testing even with 1"<< hwlib::endl;
    hwlib::cout << "Result = ";
    result = int(even(1));
    hwlib::cout << result;
    hwlib::cout << " : Should be 0\n";
    hwlib::cout << hwlib::endl;
    if (result == 0){
        count += 1;
    }

    hwlib::cout << "passed: " << count << " out of 6 tests for even" << hwlib::endl;
    return count;

}

int testodd(){
    int count = 0;
    int result = 0;
    hwlib::cout << "Testing odd with 0"<< hwlib::endl;
    hwlib::cout << "Result = ";
    result = int(odd(0));
    hwlib::cout << result;
    hwlib::cout << " : Should be 0\n";
    hwlib::cout << hwlib::endl;
    if (result == 0){
        count += 1;
    }

    hwlib::cout << "Testing odd with 9"<< hwlib::endl;
    hwlib::cout << "Result = ";
    result = int(odd(9));
    hwlib::cout << result;
    hwlib::cout << " : Should be 1\n";
    hwlib::cout << hwlib::endl;
    if (result == 1){
        count += 1;
    }

    hwlib::cout << "Testing odd with 8"<< hwlib::endl;
    hwlib::cout << "Result = ";
    result = int(odd(8));
    hwlib::cout << result;
    hwlib::cout << " : Should be 0\n";
    hwlib::cout << hwlib::endl;
    if (result == 0){
        count += 1;
    }

    hwlib::cout << "Testing odd with -9"<< hwlib::endl;
    hwlib::cout << "Result = ";
    result = int(odd(-9));
    hwlib::cout << result;
    hwlib::cout << " : Should be 1\n";
    hwlib::cout << hwlib::endl;
    if (result == 1){
        count += 1;
    }

    hwlib::cout << "Testing odd with -8"<< hwlib::endl;
    hwlib::cout << "Result = ";
    result = int(odd(-8));
    hwlib::cout << result;
    hwlib::cout << " : Should be 0\n";
    hwlib::cout << hwlib::endl;
    if (result == 0){
        count += 1;
    }

    hwlib::cout << "Testing odd with 1"<< hwlib::endl;
    hwlib::cout << "Result = ";
    result = int(odd(1));
    hwlib::cout << result;
    hwlib::cout << " : Should be 1\n";
    hwlib::cout << hwlib::endl;
    if (result == 1){
        count += 1;
    }



    hwlib::cout << "passed: " << count << " out of 6 tests for odd" << hwlib::endl;
    return count;
}

int testSommig(){
    int count = 0;
    int result = 0;

    hwlib::cout << "Testing sommig with 0"<< hwlib::endl;
    hwlib::cout << "Result = ";
    result = int(sommig(0));
    hwlib::cout << result;
    hwlib::cout << " : Should be 0\n";
    hwlib::cout << hwlib::endl;
    if (result == 0){
        count += 1;
    }

    hwlib::cout << "Testing sommig with 9"<< hwlib::endl;
    hwlib::cout << "Result = ";
    result = int(sommig(9));
    hwlib::cout << result;
    hwlib::cout << " : Should be 45\n";
    hwlib::cout << hwlib::endl;
    if (result == 45){
        count += 1;
    }

    hwlib::cout << "Testing sommig with -9"<< hwlib::endl;
    hwlib::cout << "Result = ";
    result = int(sommig(-9));
    hwlib::cout << result;
    hwlib::cout << " : Should be 0\n";
    hwlib::cout << hwlib::endl;
    if (result == 0){
        count += 1;
    }

    hwlib::cout << "Testing sommig with 1"<< hwlib::endl;
    hwlib::cout << "Result = ";
    result = int(sommig(1));
    hwlib::cout << result;
    hwlib::cout << " : Should be 1\n";
    hwlib::cout << hwlib::endl;
    if (result == 1){
        count += 1;
    }


    hwlib::cout << "passed: " << count << " out of 4 tests for sommig" << hwlib::endl;
    return count;
}

int testCheese(){
    int count = 0;
    int result = 0;

    hwlib::cout <<"Testing fillListWithCheese with list of length 100"<< hwlib::endl;
    hwlib::cout <<"Result = ";
    int cheeselijst[100];
    fillListWithCheese(cheeselijst, 100);
    for (int i = 0; i < 100; i++){
        hwlib::cout << cheeselijst[i] << " ";
    }
    hwlib::cout << hwlib::endl;


    int mijnlijst[100];
    for (int i = 0; i < 100; i++){
        mijnlijst[i] = i;
    }
    hwlib::cout <<"CompareList = ";
    for (int i = 0; i < 100; i++){
        hwlib::cout << mijnlijst[i] << " ";
    }

    hwlib::cout << hwlib::endl;
    bool equals = true;
    for (int i = 0; i < 100; i++){
        if (cheeselijst[i] != mijnlijst[i]){
            equals = false;
            break;
        }
    }

    if (equals){
        count += 1;
        hwlib::cout << "the lists are equal" << hwlib::endl;
    }else{
        hwlib::cout << "the lists are not equal" << hwlib::endl;
    }

    hwlib::cout << hwlib::endl;

    hwlib::cout << hwlib::endl;

    hwlib::cout <<"Testing getCheese with index 10"<< hwlib::endl;
    hwlib::cout <<"Result = ";
    result = int(getCheese(mijnlijst, 100, 10));
    hwlib::cout << result;
    hwlib::cout <<" : Should be 10\n"<< hwlib::endl << hwlib::endl;
    if (result == 10){
        count += 1;
    }

    hwlib::cout <<"Testing getCheese with index -9"<< hwlib::endl;
    hwlib::cout <<"Result = ";
    result = int(getCheese(mijnlijst, 100, -9));
    hwlib::cout << result;
    hwlib::cout <<" : Should be 91\n"<< hwlib::endl << hwlib::endl;
    if (result == 91){
        count += 1;
    }

    hwlib::cout <<"Testing getCheese with index 105"<< hwlib::endl;
    hwlib::cout <<"Result = ";
    result = int(getCheese(mijnlijst, 100, 105));
    hwlib::cout << result;
    hwlib::cout <<" : Should be 0\n"<< hwlib::endl << hwlib::endl;
    if (result == 0){
        count += 1;
    }

    hwlib::cout <<"Testing getCheese with index 0"<< hwlib::endl;
    hwlib::cout <<"Result = ";
    result = int(getCheese(mijnlijst, 100, 0));
    hwlib::cout << result;
    hwlib::cout <<" : Should be 0\n"<< hwlib::endl << hwlib::endl;
    if (result == 0){
        count += 1;
    }
    hwlib::cout << "passed: " << count << " out of 5 tests for fillListWithCheese and getCheese" << hwlib::endl;
    return count;

}



int main() {
// write your code here
    hwlib::wait_ms( 1000 );
    hwlib::cout << "Testen op foutieve types kan niet aangezien de functies worden gebruikt via extern C delcaraties die types aangeven\n";
    int count = 0;
    count += testSommig();
    count += testeven();
    count += testodd();
    count += testCheese();
    hwlib::cout << "Passed: " << count <<" Tests out of 21 tests total" << hwlib::endl;
    hwlib::wait_ms( 500 );
    int n = 0;
    while(true){n += 1;}
}