from gl import *
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.arrays import vbo
from string import *
from ctypes import c_void_p

strFragmentShader = """
#version 130
smooth in vec4 theColor;
out vec4 outputColor;
void main()
{
    outputColor = theColor;
}
"""

strVertexShader = """
#version 130
in vec4 position;
in vec4 color;
uniform float loopDuration; 
uniform float time;
smooth out vec4 theColor;
void main()
{
    float timeScale = 3.14159f * 2.0f / loopDuration;
    float currTime = mod(time, loopDuration);
    vec4 totalOffset = vec4(cos(currTime*timeScale)*0.5f, 
                            0.0f, 
                            sin(currTime*timeScale)*0.5f, 
                            0.0f);
    gl_Position = position;// + totalOffset;
    theColor = color;
}
"""

def InitializeVertexBuffer():
    global positionBufferObject
    ReadModel('gargoyle_color.obj')
    positionBufferObject = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, positionBufferObject)
    glBufferData(GL_ARRAY_BUFFER, vertex_Positions_Colors, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glUseProgram(theProgram)
    glUniform1f(timeLocation, glutGet(GLUT_ELAPSED_TIME)/1000.)
    glBindBuffer(GL_ARRAY_BUFFER, positionBufferObject)
    glEnableVertexAttribArray(0)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(0, 4, GL_FLOAT, True, 0, c_void_p(0))
    glVertexAttribPointer(1, 4, GL_FLOAT, True, 0, c_void_p(16*v))
    glDrawArrays(GL_TRIANGLES, 0, v)
    glDisableVertexAttribArray(0)
    glDisableVertexAttribArray(1)
    glUseProgram(0)
    glutSwapBuffers()
    glutPostRedisplay()
    
def reshape(w,h):
    glViewport(0, 0, w, h)

def InitializeProgram():
    global theProgram, timeLocation, loopDurationLocation
    VERTEX_SHADER = compileShader(strVertexShader, GL_VERTEX_SHADER)
    FRAGMENT_SHADER = compileShader(strFragmentShader, GL_FRAGMENT_SHADER)
    theProgram = compileProgram(VERTEX_SHADER, FRAGMENT_SHADER)
    timeLocation = glGetUniformLocation(theProgram, "time") # Define the uniform variable 'time' in shaders, implemented for animation
    loopDurationLocation = glGetUniformLocation(theProgram, "loopDuration") #Define the uniform variable 'loopDuration' in shaders, implemented for animation
    glUseProgram(theProgram)
    glUniform1f(loopDurationLocation, 5.) #Define the number
    glUseProgram(0)

def ReadModel(FileName):
    #global vArr,vcArr,fArr,
    global vertex_Positions_Colors,v,c
    vArr=[]
    vcArr=[]
    fArr=[]
    vertex_Positions_Colors=[]
    fp=open(FileName,"r");
    lines = fp.readlines()
    fp.close()
    for i in range(len(lines)):
        DataBuffer = lines[i]
        DataBuffer=split(DataBuffer)
        if DataBuffer[0]=='vc':
               vcArr.append([atof(DataBuffer[1]),atof(DataBuffer[2]),atof(DataBuffer[3])])
        elif DataBuffer[0]=='v':
               vArr.append([atof(DataBuffer[1]),atof(DataBuffer[2]),atof(DataBuffer[3])])
        elif DataBuffer[0]=='f':
               fArr.append([atoi(DataBuffer[1]),atoi(DataBuffer[2]),atoi(DataBuffer[3])])
    max0=0;
    max1=0;
    max2=0;
    min0=0;
    min1=0;
    min2=0;
    for i in range(0,len(vArr)):
        if (vArr[i][0]>max0):
            max0=vArr[i][0];
        if (vArr[i][0]<min0):
            min0=vArr[i][0];
        if (vArr[i][1]>max1):
            max1=vArr[i][1];
        if (vArr[i][1]<min1):
            min1=vArr[i][1];
        if (vArr[i][2]>max2):
            max2=vArr[i][2];
        if (vArr[i][2]<min2):
            min2=vArr[i][2];
    print(max0,max1,max2,min0,min1,min2)
    for i in range(0,len(vArr)):
        vArr[i][0]=2*(vArr[i][0]-min0)/(max0-min0)-1;
        vArr[i][1]=2*(vArr[i][1]-min1)/(max1-min1)-1;
        vArr[i][2]=2*(vArr[i][2]-min2)/(max2-min2)-1;
    point=[]
    color=[]
    for i in range(0,len(fArr)):
        point.append(vArr[fArr[i][0]-1]+[1.])
        point.append(vArr[fArr[i][1]-1]+[1.])
        point.append(vArr[fArr[i][2]-1]+[1.])
        color.append(vcArr[fArr[i][0]-1]+[1.])
        color.append(vcArr[fArr[i][1]-1]+[1.])
        color.append(vcArr[fArr[i][2]-1]+[1.])
    vertex_Positions_Colors = array(point+color,dtype="float32")
    v=len(point)
    c=len(color)

def init():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(500,500)
    glutCreateWindow("Window")
    InitializeProgram()
    InitializeVertexBuffer()
    glClearColor(0.,0.,0.,0.)

def main():
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glEnable(GL_DEPTH_TEST)
    #glMatrixMode(GL_PROJECTION)
    #glLoadIdentity()
    #glOrtho(-3.0, 3.0, -3.0, 3.0, -3.0, 3.0)
    #glMatrixMode(GL_MODELVIEW)
    print(v,c)
    glutMainLoop()

main()
