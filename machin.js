
for (let i=0 ; i < 26 ; i++){
    console.log(
      "\t\t #"+String.fromCharCode(i + 97)+" \n"+
      "\t\tif xi.GetState(0)[1].B.B and state["+i+"] == 0:\n"+
          "\t\t\tkeyboard.press('"+String.fromCharCode(i + 97) +"')\n"+
          "\t\t\tstate["+i+"] = 1\n"+
          "\t\tif xi.GetState(0)[1].B.B == 0 and state["+i+"] == 1:\n"+
          "\t\t\tstate["+i+"] = 0"
    );
  }