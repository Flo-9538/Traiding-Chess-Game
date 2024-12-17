package ClasseMetier;

import java.util.ArrayList;

public class piece {
    private int idB; //id sur le plateaux
    private int idP; //id de la pièce
    private ArrayList<int[]> mouvement; //les vecteur mouvement en [(x,y),…]
    private String Nom; //nom de la pièce
    private String pouvoirs; // nom du pouvoirs 
    private int x; // position sur le plateaux en x 
    private int y; // position sur le plateaux en y
    private String image; // url de l'image
    private static int Nbp=0; // pour comptre le nombre de pièce 

    public piece(int idP, ArrayList<int[]> mouvement, String pouvoirs, String Nom, int x, int y, String image){
        this.idP=idP;
        this.idP= Nbp;
        this.mouvement=mouvement;
        this.pouvoirs=pouvoirs;
        this.Nom=Nom;
        this.x=x;
        this.y=y;
        this.image=image;
        piece.Nbp +=1;
    }

    public int getX(){
        return this.x;
    }

    public int getY(){
        return this.y;
    }

    public String getimage(){
        return this.image;
    }

    public void setX(int X){
        this.x= X;
    }

    public void setY(int Y){
        this.x= Y;
    }

    public ArrayList<int[]> caseAtegnable(){
        ArrayList<int[]> caseAtegnable = new ArrayList<int[]>();
        for (int[] mouv: this.mouvement){
            if (this.x+mouv[0]>0 && this.y+mouv[1]>0 && this.x+mouv[0]<0 && this.y+mouv[1]>0){
                int[] mouve = {this.x+mouv[0],this.y+mouv[1]};
                caseAtegnable.add(mouve);
            }
        }
        return caseAtegnable;
    }

    




    
}
