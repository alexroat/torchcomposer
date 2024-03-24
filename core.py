import torch
import torch.nn as nn
import torch.optim as optim
from torch.nn import functional as F
from torch.utils.data import DataLoader
from torchvision import transforms


class DynModule(nn.Module):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.layers={}
        self.setLayer("input",None,{})
        self.setLayer("output",lambda x:x,{"x":"input"})
    def forward(self, x):
        results={"input":x}
        def compute(name):
            if name in results:
                return results[name]
            args={k:compute(v) for k,v in self.layers[name]["inputs"].items()}
            r=self.layers[name]["fn"](**args)
            results[name]=r
            return r
        return compute("output")
    def setLayer(self,name,fn,inputs={}):
        self.layers[name]={"fn":fn,"inputs":inputs}
    def from_dict(self,d):
        pass
        
        
        
dm=DynModule()

c=dm.forward("ciao")

print(c)




    