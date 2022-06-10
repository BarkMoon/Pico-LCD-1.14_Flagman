// This program is originally from http://picceri.blogspot.com/2018/05/24bitbmprgb565binctxt-7-1_31.html by iwasan1936
// I added mode 8 & 9, recolor and pytxt.

#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <fstream>
#include <string>
#include <string.h>

using namespace std;

class BMP{
public:
  unsigned int w;
  int h;
  unsigned int fourmod;
  unsigned int offset;
  char name[40];

  BMP(){
    fourmod = 0;
    offset = 0;
    w = 0;
    h = 0;
  }
  void get_offset(ifstream& inf){
    inf.seekg(0xA , ios_base::beg);
    inf.read((char*)&offset,4);
    inf.seekg(offset , ios_base::beg);
  }
  void get_wh_and_fourmod(ifstream& inf){
    unsigned char buf[10];
    inf.seekg(0xE, ios_base::beg);
    inf.read((char*)buf,1);

    if(buf[0] == 40){
      inf.seekg(0x12, ios_base::beg);
      inf.read((char*)&w,4);
      inf.read((char*)&h,4);
      //h = (buf[1] << 8) + buf[0];
    } else {
      short int hshort;
      inf.seekg(0x12, ios_base::beg);
      inf.read((char*)&w,2);
      inf.read((char*)&hshort,2);
      h = hshort;
    }
    if(((w*3) % 4) != 0){
      fourmod = 4 - ((w*3) % 4);
    }
  }
};

unsigned int convert_bmp_to_bin(ofstream &of , ifstream& inf , BMP& bmp);
unsigned int press_bin_to_bin(ofstream &of , ifstream& inf);
void bin_to_txt(ifstream& inf, ofstream& of ,unsigned int n);
unsigned int recolor_convert_bmp_to_bin(ofstream &of , ifstream& inf , BMP& bmp);
void bin_to_pytxt(ifstream& inf, ofstream& of);

int main(){
  char if_name[70] , of_name[70],name[70];
  int mode;

  ifstream inf;
  ofstream of;
  BMP bmp;

  cout << "\n Select mode.\n";
  cout << "1: Just convert 24bit BMP to RGB565 bin file. \n";
  cout << "2: Convert and compress 24bit BMP to RGB565 bin file. \n";
  cout << "3: Output converted RGB565 bin file from 24bit BMP as C array. \n";
  cout << "4: Output converted and compressed RGB565 bin file from 24bit BMP as C array. \n";
  cout << "5: Output txt as C array from bin file . \n";
  cout << "6: Compress and Output txt as C array from bin file . \n";
  cout << "7: Compress bin file and output to bin file. \n";
  cout << "8: Output converted RGB565 bin file from 24bit BMP as Python bytearray. \n";
  cout << "9: Recolor and output converted RGB565 bin file from 24bit BMP as Python bytearray. \n";
  cout << "Mode : ";
  cin >> mode;

  if(mode == 5 || mode == 6 || mode == 7){
    cout << "Enter the bin file name : ";
    cin >> of_name;
  }
  if(mode == 1 || mode == 2 || mode == 3 || mode == 4 || mode == 8){
    cout << "Enter the BMP file name : ";
    cin >> if_name;
    inf.open(if_name ,ios::binary);
    if(inf.fail()){
      cout << "Could not open BMP \n";
      return -1;
    }
    bmp.get_offset(inf);
    bmp.get_wh_and_fourmod(inf);
    cout << bmp.w << ' ' << bmp.h << endl;
    sprintf(of_name ,"%s.bin" ,if_name);
    of.open(of_name ,ios::binary);
    if(of.fail()){
      cout << "Could not make bin file. \n";
    }
    cout << convert_bmp_to_bin(of,inf,bmp) << endl;
    inf.close();
    of.close();
  }
  if(mode == 9){
    cout << "Enter the BMP file name : ";
    cin >> if_name;
    inf.open(if_name ,ios::binary);
    if(inf.fail()){
      cout << "Could not open BMP \n";
      return -1;
    }
    bmp.get_offset(inf);
    bmp.get_wh_and_fourmod(inf);
    cout << bmp.w << ' ' << bmp.h << endl;
    sprintf(of_name ,"%s.bin" ,if_name);
    of.open(of_name ,ios::binary);
    if(of.fail()){
      cout << "Could not make bin file. \n";
    }
    cout << recolor_convert_bmp_to_bin(of,inf,bmp) << endl;
    inf.close();
    of.close();
  }
  if(mode == 2 || mode == 4 || mode == 6 || mode == 7){
    inf.open(of_name ,ios::binary);
    if(inf.fail()){
      cout << "Could not open bin \n";
      return -1;
    }
    sprintf(name ,"pressed_%s" ,of_name);
    strcpy(of_name ,name);
    of.open(of_name ,ios::binary);
    if(of.fail()){
      cout << "Could not make bin file. \n";
    }
    press_bin_to_bin(of,inf);
    inf.close();
    of.close();
  }
  if(mode == 3 || mode == 4 || mode == 5 || mode == 6){
    unsigned int n;
    cout << "\n\nHow often do you want to insert new line? : ";
    cin >> n;
    inf.open(of_name ,ios::binary);
    if(inf.fail()){
      cout << "Could not open bin \n";
      return -1;
    }
    sprintf(name ,"%s.txt" ,of_name);
    strcpy(of_name ,name);
    of.open(of_name);
    if(of.fail()){
      cout << "Could not make bin file. \n";
    }
    bin_to_txt(inf,of,n);
    inf.close();
    of.close();
  }
  if(mode == 8 || mode == 9){
    inf.open(of_name ,ios::binary);
    if(inf.fail()){
      cout << "Could not open bin \n";
      return -1;
    }
    sprintf(name ,"%s.txt" ,of_name);
    strcpy(of_name ,name);
    of.open(of_name);
    if(of.fail()){
      cout << "Could not make bin file. \n";
    }
    bin_to_pytxt(inf,of);
    inf.close();
    of.close();
  }

/*
  cout << "\nBin file size = " << bytes << "bytes\n";
  of.close();
  inf.close();
  inf.open(of_name ,ios::binary);

  if(mode == 2){

    cout << "\n\nHow often do you want to insert new line?\n";
    cout << "* The number you will input must be multiples of 2\n";


  } else if(mode == 3){


    cout << "\nThe number how array elements has = " << bytes_pressed << endl;
    printf("Compression ratio = %5.2f\n" ,bytes_pressed/(float)bytes);

  }
  cout << "\nDone\n";
  inf.close();
  of.close();
  */
  cout << "DONE";
  return 0;
}


unsigned int convert_bmp_to_bin(ofstream &of , ifstream& inf , BMP& bmp){
  unsigned char buf[10];
  unsigned int bytes = 0;
  inf.seekg(bmp.offset , ios_base::beg);
  cout << "offset:" << bmp.offset << endl;
  cout << "fourmod:" << bmp.fourmod << endl;
  for(unsigned int i=0;i<bmp.h;i++){
    unsigned int seekpoint = (bmp.h - i - 1) * bmp.w * 2;
    of.seekp(seekpoint, ios_base::beg);
    for(unsigned int j=0;j<bmp.w*2;j+=2){
      //char str[40];
      unsigned char tmp,r,g,b;
      //unsigned short buf[5];
      inf.read((char*)buf,3);

      r = buf[2] >> 3;
      g = buf[1] >> 2;
      b = buf[0] >> 3;

      tmp = (g << 5) + b;
      //tmp = ((buf[1] << 5) & 0b11100000) + ((buf[0] >> 3) & 0b11111);
      //tmp = ((buf[1] & 0b111) << 5) + ((buf[0] >> 3) & 0b11111);
      of.write((char*)&tmp,1);


      tmp = (r << 3) + (g >> 3);
      //tmp = ((buf[2] << 3) & 0b11111000) + ((buf[1] >> 5) & 0b111);
      //tmp = ((buf[2] & 0b11111) << 3) + ((buf[1] >> 5) & 0b111);
      of.write((char*)&tmp,1);
      bytes += 2;
    }
    inf.seekg(bmp.fourmod, ios_base::cur);
  }
  return bytes;
}


unsigned int press_bin_to_bin(ofstream &of , ifstream& inf){
  unsigned int bytes_pressed=0,bytes=0;
  unsigned char count_byte = 1;
  unsigned char tmp[2];
  unsigned char buf[10];

  inf.read((char*)tmp ,2);
  bytes += 2;
  while(1){
    inf.read((char*)buf ,2);
    if(inf.eof()){
      of.write((char*)&count_byte,1);
      of.write((char*)&tmp[0],2);
      bytes_pressed += 3;
      break;
    }
    bytes += 2;
    if(count_byte++ == 255 || tmp[0] != buf[0] || tmp[1] != buf[1]){
      count_byte--;
      of.write((char*)&count_byte,1);
      of.write((char*)&tmp[0],2);
      tmp[0] = buf[0]; tmp[1] = buf[1];
      count_byte = 1;
      bytes_pressed += 3;
    }
  }
  printf("Compression ratio = %5.2f\n" ,bytes_pressed/(float)bytes);
  return bytes_pressed;
}


void bin_to_txt(ifstream& inf, ofstream& of ,unsigned int n){
  unsigned int counter = 0 , elements = 2;
  char str[20];
  unsigned char tmp[2];
  unsigned char buf[10];
  of << "{\r\n";
  inf.read((char*)tmp ,1);
  while(!inf.eof()){
    inf.read((char*)buf ,1);
    if(inf.eof()){
      sprintf(str,"0x%02x\r\n};",(tmp[0]));
      of << str;
      break;
    }
    elements++;
    sprintf(str,"0x%02x,",(tmp[0]));
    of << str;
    if(++counter == n){
      of << "\r\n";
      counter = 0;
    }
    tmp[0] = buf[0];
  }
  cout << "\nHow many elements array has = " << elements << endl;
}


unsigned int recolor_convert_bmp_to_bin(ofstream &of , ifstream& inf , BMP& bmp){
  unsigned char buf[10];
  unsigned int bytes = 0;
  inf.seekg(bmp.offset , ios_base::beg);
  cout << "offset:" << bmp.offset << endl;
  cout << "fourmod:" << bmp.fourmod << endl;
  for(unsigned int i=0;i<bmp.h;i++){
    unsigned int seekpoint = (bmp.h - i - 1) * bmp.w * 2;
    of.seekp(seekpoint, ios_base::beg);
    for(unsigned int j=0;j<bmp.w*2;j+=2){
      //char str[40];
      unsigned char tmp,r,g,b;
      //unsigned short buf[5];
      inf.read((char*)buf,3);

      r = buf[2] >> 2;
      g = buf[1] >> 3;
      b = buf[0] >> 3;

      tmp = (r << 5) + g;
      //tmp = ((buf[1] << 5) & 0b11100000) + ((buf[0] >> 3) & 0b11111);
      //tmp = ((buf[1] & 0b111) << 5) + ((buf[0] >> 3) & 0b11111);
      of.write((char*)&tmp,1);


      tmp = (b << 3) + (r >> 3);
      //tmp = ((buf[2] << 3) & 0b11111000) + ((buf[1] >> 5) & 0b111);
      //tmp = ((buf[2] & 0b11111) << 3) + ((buf[1] >> 5) & 0b111);
      of.write((char*)&tmp,1);
      bytes += 2;
    }
    inf.seekg(bmp.fourmod, ios_base::cur);
  }
  return bytes;
}


void bin_to_pytxt(ifstream& inf, ofstream& of){
  unsigned int elements = 2;
  char str[20];
  unsigned char tmp[2];
  unsigned char buf[10];
  of << "b\"";
  inf.read((char*)tmp ,1);
  while(!inf.eof()){
    inf.read((char*)buf ,1);
    if(inf.eof()){
      sprintf(str,"\\x%02x\"",(tmp[0]));
      of << str;
      break;
    }
    elements++;
    sprintf(str,"\\x%02x",(tmp[0]));
    of << str;
    tmp[0] = buf[0];
  }
  cout << "\nHow many elements array has = " << elements << endl;
}
