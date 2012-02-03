# dancer.py
# JM Kinser
# 16 December 1999

import Tkinter
import Image
import ImageTk
import ImageEnhance

class Dancer:
    "The dancer image machine"
    def __init__( self,JPY ):
        self.rt = Tkinter.Tk()
        self.rt.withdraw()
        self.tp = [ Tkinter.Toplevel(self.rt)] 
        self.tp[0].title('Image #0')
        self.mg = [ Image.open( JPY + 'wet_floorboard.jpg')]
        self.ph = [ ImageTk.PhotoImage( self.mg[0]) ]
        self.lb = [ Tkinter.Label( self.tp[0], image = self.ph[0] ) ]
        # use Button-2 for point and shoot
        self.lb[0].bind( "<Button-3>", self.PointShoot )
        self.lb[0].pack( anchor='nw', side='left')
    def Show( self, N=0 ):
        # used by many of the routines here.
        self.ph[N] = ImageTk.PhotoImage( self.mg[N])
        self.lb[N].destroy()
        self.lb[N] = Tkinter.Label( self.tp[N], image=self.ph[N])
        self.lb[N].bind( "<Button-3>", self.PointShoot )
        self.lb[N].pack(anchor='nw', side='left')
    def Load( self, filename, N=0):
        self.mg[N] = Image.open( filename )
        self.Show( N )
    def Add( self, filename):
        self.mg.append( Image.open( filename) )
        N = len(self.mg)-1
        self.tp.append( Tkinter.Toplevel(self.rt))
        self.tp[N].title( 'Image #' + str(N))
        self.ph.append( ImageTk.PhotoImage( self.mg[N]))
        self.lb.append( Tkinter.Label(self.tp[N], image=self.ph[N]))
        self.lb[N].bind( "<Button-3>", self.PointShoot )
        self.lb[N].pack( anchor='nw', side='left')
    def Paste( self, mg, N=0):
        self.mg[N] = mg
        self.Show( N )
    def Destroy(self, N ):
        # This will change the numbers of all subsequent images
        del self.mg[N]
        del self.ph[N]
        self.lb[N].destroy()
        self.tp[N].destroy()
        del self.lb[N]
        del self.tp[N]
        # rename
        for i in range( 0,len(self.mg)):
            self.tp[i].title( 'Image #'+str(i))
    def Scale( self, factor, N=0):
        s = self.mg[N].size
        t = ( int(float(s[0])*factor),int(float(s[1])*factor))
        self.mg[N] = self.mg[N].resize(t)
        self.Paste( self.mg[N], N)
    def Crop( self, ulcoords, lrcoords, N=0, M=0):
        # use N and M to cut one image into another
        # coords for box are left, upper, right, lower
        box = (ulcoords[0], ulcoords[1], lrcoords[0], lrcoords[1])
        if M > len(self.mg):
            self.append( self.mg[N].crop( box ))
        else:
            self.mg[M] = self.mg[N].crop( box )
        self.Show(M)
    def PointShoot(self, event ):
        # who has focus
        #a = self.rt.winfo_children()
        print (event.x, event.y), self.ph[0]._PhotoImage__photo.get( event.x, event.y)
    def Brightness( self, val, N=0 ):
        a = ImageEnhance.Brightness( self.mg[N] )
        self.mg[N] = a.enhance( val )
        self.Show(N)
        
        
        
