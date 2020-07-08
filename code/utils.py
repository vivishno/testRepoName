import os
import sys
import importlib
import json
from json import JSONDecodeError
from azure.mgmt.resource.resources.models import DeploymentMode

class ActionDeploymentError(Exception):
    pass

class AMLConfigurationException(Exception):
    pass

class ResourceManagementError(Exception):
    pass

class CredentialsVerificationError(Exception):
    pass

class TemplateParameterException(Exception):
    pass

class InvalidDeploymentModeException(Exception):
    pass

def get_template_parameters(template_params_file,mapped_params):
    parameters={}
    try:
        if len(template_params_file)!=0:
            template_params_file_path = os.path.join(".cloud", ".azure", template_params_file)
            with open(template_params_file_path,"r") as f:
                jsonobject = json.load(f);
            parameters=jsonobject["parameters"]
            
        for k in mapped_params:
            parameters[k]={}
            parameters[k]["value"] = mapped_params[k]
   
    except JSONDecodeError:
        print("::error::Please check the parameter file for errors")
        raise TemplateParameterException(f"Incorrect or poorly formed template parameters")
        
    return parameters

def get_deploy_mode_obj(deployment_mode):
    if deployment_mode=="Incremental":
        return DeploymentMode.incremental
    elif deployment_mode=="Complete":
        return DeploymentMode.complete
    else:
        raise InvalidDeploymentModeException(f"Please provide deployment mode as \"Incremental\" or \"Complete\" only.")


def required_parameters_provided(parameters, keys, message="Required parameter not found in your parameters file. Please provide a value for the following key(s): "):
    missing_keys = []
    for key in keys:
        if key not in parameters:
            err_msg = f"{message} {key}"
            print(f"::error::{err_msg}")
            missing_keys.append(key)
    if len(missing_keys) > 0:
        raise AMLConfigurationException(f"{message} {missing_keys}")


def mask_parameter(parameter):
    print(f"::add-mask::{parameter}")

