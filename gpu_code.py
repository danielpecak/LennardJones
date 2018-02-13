from biblioteka import stale

# __device__ - can be called internally by the GPU device
# __global__ - can be called by a program, returns always VOID
# dtoh - device to host oraz htod - host to device
# Transfering data to and from the GPU device

source = """
__device__ float2 odleglosc(float rx, float ry)
{
  float2 r;
  float b = """+str(stale.boxsize)+""";
  r.x = rx;
  r.y = ry;
  if (r.x > b/2)
  {
    r.x -= b;
  };
  if (r.x < -b/2)
  {
    r.x += b;
  };
  if (r.y > b/2)
  {
    r.y -= b;
  };
  if (r.y < -b/2)
  {
    r.y += b;
  };
  return r;
}

__device__ float2 pbc(float rx, float ry)
{
  float2 r;
  float b = """+str(stale.boxsize)+""";
  r.x = rx;
  r.y = ry;
  if (r.x > b)
  {
    r.x -= b;
  };
  if (r.x < -b)
  {
    r.x += b;
  };
  if (r.y > b)
  {
    r.y -= b;
  };
  if (r.y < -b)
  {
    r.y += b;
  };
  return r;
}

__device__ float potencjal(float rx, float ry)
{
  float rc="""+str(stale.rc)+""", sigma="""+str(stale.sigma)+""", eps="""+str(stale.eps)+""";
  float2 r;
  r = odleglosc(rx,ry);
  float rn = sqrt(r.x*r.x+r.y*r.y);
  if (rn < rc)
  {
    return 4*eps*(pow((sigma/rn),12)-pow((sigma/rn),6));
  }
  else
  {
    return 0;
  }
}

__device__ float2 sila(float rx, float ry)
{
  float rc="""+str(stale.rc)+""", sigma="""+str(stale.sigma)+""", eps="""+str(stale.eps)+""";
  float2 f;
  f.x = 0;
  f.y = 0;
  float2 r;
  r = odleglosc(rx,ry);
  float rn = sqrt(r.x*r.x+r.y*r.y);
  if (rn < rc)
  {
    f.x = r.x/rn*48*eps/sigma*(pow((sigma/rn),13)-0.5*pow((sigma/rn),7));
    f.y = r.y/rn*48*eps/sigma*(pow((sigma/rn),13)-0.5*pow((sigma/rn),7));
    return f;
  }
  else
  {
    return f;
  }
}



__global__ void energy(float *px, float *py, float *en)
{
  int idx = threadIdx.x ;
  en[idx] = (px[idx]*px[idx] + py[idx]*py[idx])/2 ;
}

__global__ void polKroku(float *v,float *px,float *py,float *fx,float *fy)
{
  int idx = threadIdx.x;
  v[idx] = (pow(px[idx] + fx[idx]*"""+str(stale.deltat)+"""/2,2) + pow(py[idx] + fy[idx]*"""+str(stale.deltat)+"""/2,2))/2;
}

__global__ void fupdate(float *rx,float *ry,float *fx,float *fy)
{
  int idx = threadIdx.x;
  int n = blockDim.x;
  float2 silaWyp;
  silaWyp.x = 0;
  silaWyp.y = 0;
  for(int i = 0; i < n;i++)
  {
    if (idx != i)
    {
      silaWyp.x = silaWyp.x - sila(rx[i] - rx[idx],ry[i] - ry[idx]).x;
      silaWyp.y = silaWyp.y - sila(rx[i] - rx[idx],ry[i] - ry[idx]).y;
    };
  };
  fx[idx] = silaWyp.x;
  fy[idx] = silaWyp.y;
}

__global__ void leapfrog(float *px,float *py,float *rx,float *ry,float *fx,float *fy,float eta)
{
  int idx = threadIdx.x;
  float dt = """+str(stale.deltat)+""";
  px[idx] = (px[idx]*(2*eta-1) + eta*dt*fx[idx]);
  py[idx] = (py[idx]*(2*eta-1) + eta*dt*fy[idx]);
  float2 rxy = pbc(px[idx]*dt + rx[idx],py[idx]*dt + ry[idx]);
  rx[idx] = rxy.x;
  ry[idx] = rxy.y;
}

__global__ void repopulate(float *rx,float *ry,float *nl, float rn)
{
  int idx  = threadIdx.x;
  for(int i = 0; i < int(rn); i++)
  {
    nl[int(rn)*idx + i] = -1;
  };
  int nextFree = 0;
  for(int i = 0; i < blockDim.x; i++)
  {
    if (idx != i)
    {
      float2 odl = odleglosc(rx[idx]-rx[i],ry[idx]-ry[i]);
      float nodl = sqrt(pow(odl.x,2) + pow(odl.y,2));
      if ( nodl < float("""+str(stale.rcc)+"""))
      {
        nl[int(rn)*idx + nextFree] = i;
        nextFree += 1;
      }
    }
  };
}

"""
