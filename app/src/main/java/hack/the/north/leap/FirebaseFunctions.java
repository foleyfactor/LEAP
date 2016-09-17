package hack.the.north.leap;

import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

/**
 * Created by Alex on 2016-09-17.
 */
public class FirebaseFunctions {

    //Usage: setFist(b), which sets the fist property in the firebase
    public void setFist(boolean b) {
        DatabaseReference ref = FirebaseDatabase.getInstance().getReference("").child("fist");
        ref.setValue(b);
    }

    //Usage: setDelta(x,y), which sets deltaX and deltaY respectively.
    public void setDelta(double x, double y) {
        DatabaseReference refx = FirebaseDatabase.getInstance().getReference("").child("deltaX");
        DatabaseReference refy = FirebaseDatabase.getInstance().getReference("").child("deltaY");

        refx.setValue(x);
        refy.setValue(y);
    }
}
