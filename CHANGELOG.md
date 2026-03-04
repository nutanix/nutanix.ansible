# Nutanix\.Ncp Release Notes

**Topics**

- <a href="#v2-4-0">v2\.4\.0</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#minor-changes">Minor Changes</a>
    - <a href="#breaking-changes--porting-guide">Breaking Changes / Porting Guide</a>
    - <a href="#bugfixes">Bugfixes</a>
    - <a href="#new-plugins">New Plugins</a>
        - <a href="#inventory">Inventory</a>
    - <a href="#new-modules">New Modules</a>
- <a href="#v2-3-0">v2\.3\.0</a>
    - <a href="#release-summary-1">Release Summary</a>
    - <a href="#minor-changes-1">Minor Changes</a>
    - <a href="#bugfixes-1">Bugfixes</a>
    - <a href="#new-modules-1">New Modules</a>
- <a href="#v2-2-0">v2\.2\.0</a>
    - <a href="#release-summary-2">Release Summary</a>
    - <a href="#minor-changes-2">Minor Changes</a>
    - <a href="#bugfixes-2">Bugfixes</a>
    - <a href="#new-modules-2">New Modules</a>
- <a href="#v2-1-1">v2\.1\.1</a>
    - <a href="#release-summary-3">Release Summary</a>
    - <a href="#bugfixes-3">Bugfixes</a>
- <a href="#v2-1-0">v2\.1\.0</a>
    - <a href="#release-summary-4">Release Summary</a>
    - <a href="#breaking-changes--porting-guide-1">Breaking Changes / Porting Guide</a>
    - <a href="#new-modules-3">New Modules</a>
- <a href="#v2-0-0">v2\.0\.0</a>
    - <a href="#release-summary-5">Release Summary</a>
    - <a href="#new-modules-4">New Modules</a>
- <a href="#v1-9-2">v1\.9\.2</a>
    - <a href="#release-summary-6">Release Summary</a>
    - <a href="#breaking-changes--porting-guide-2">Breaking Changes / Porting Guide</a>
- <a href="#v1-9-1">v1\.9\.1</a>
    - <a href="#release-summary-7">Release Summary</a>
    - <a href="#minor-changes-3">Minor Changes</a>
    - <a href="#bugfixes-4">Bugfixes</a>
- <a href="#v1-9-0">v1\.9\.0</a>
    - <a href="#minor-changes-4">Minor Changes</a>
    - <a href="#deprecated-features">Deprecated Features</a>
    - <a href="#bugfixes-5">Bugfixes</a>
    - <a href="#new-modules-5">New Modules</a>
- <a href="#v1-8-0">v1\.8\.0</a>
    - <a href="#new-modules-6">New Modules</a>
- <a href="#v1-7-0">v1\.7\.0</a>
    - <a href="#minor-changes-5">Minor Changes</a>
    - <a href="#bugfixes-6">Bugfixes</a>
- <a href="#v1-6-0">v1\.6\.0</a>
    - <a href="#new-modules-7">New Modules</a>
- <a href="#v1-5-0">v1\.5\.0</a>
    - <a href="#new-modules-8">New Modules</a>
- <a href="#v1-4-0">v1\.4\.0</a>
    - <a href="#bugfixes-7">Bugfixes</a>
    - <a href="#new-modules-9">New Modules</a>
- <a href="#v1-3-0">v1\.3\.0</a>
    - <a href="#new-modules-10">New Modules</a>
- <a href="#v1-2-0">v1\.2\.0</a>
    - <a href="#minor-changes-6">Minor Changes</a>
    - <a href="#new-modules-11">New Modules</a>
- <a href="#v1-1-0">v1\.1\.0</a>
    - <a href="#minor-changes-7">Minor Changes</a>
    - <a href="#new-modules-12">New Modules</a>
- <a href="#v1-0-0">v1\.0\.0</a>
    - <a href="#major-changes">Major Changes</a>
    - <a href="#minor-changes-8">Minor Changes</a>
    - <a href="#bugfixes-8">Bugfixes</a>
    - <a href="#new-modules-13">New Modules</a>

<a id="v2-4-0"></a>
## v2\.4\.0

<a id="release-summary"></a>
### Release Summary

Built on v4 SDKs\. Adds Key Management Server\, STIGs\, SSL Certificates\, Storage Policies\, EULA\, Dynamic Inventory and Host Inventory modules with several improvements and bug fixes\.

<a id="minor-changes"></a>
### Minor Changes

* All modules \- \[Imprv\] Add logger based on flag to enable debug logs \[\[\#294\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/294](https\://github\.com/nutanix/nutanix\.ansible/issues/294)\)\]
* ntnx\_projects \- \[Imprv\] Remove resource limit functionality from ntnx\_projects as not supported by API \[\[\#880\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/880](https\://github\.com/nutanix/nutanix\.ansible/issues/880)\)\]
* ntnx\_storage\_policies\_v2 \- \[Imprv\] Add example for storage policy \[\[\#484\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/484](https\://github\.com/nutanix/nutanix\.ansible/issues/484)\)\]
* ntnx\_vms \- \[Imprv\] add functionality to provide sysprep or cloud\-init to module ntnx\_vms via a variable instead of a file \[\[\#389\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/389](https\://github\.com/nutanix/nutanix\.ansible/issues/389)\)\]
* ntnx\_vms\_cd\_rom\_iso\_v2 \- \[Imprv\] add code enhancement for ntnx\_vms\_cd\_rom\_iso\_v2 module \[\[\#827\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/827](https\://github\.com/nutanix/nutanix\.ansible/issues/827)\)\]

<a id="breaking-changes--porting-guide"></a>
### Breaking Changes / Porting Guide

* ntnx\_projects \- \[Breaking\] Remove resource limit functionality from ntnx\_projects as not supported by API \[\[\#880\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/880](https\://github\.com/nutanix/nutanix\.ansible/issues/880)\)\]

<a id="bugfixes"></a>
### Bugfixes

* ntnx\_lcm\_config\_v2 \- \[Bug\] Remove Default Values in module ntnx\_lcm\_config\_v2 \[\[\#879\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/879](https\://github\.com/nutanix/nutanix\.ansible/issues/879)\)\]
* ntnx\_prism\_vm\_inventory \- \[Bug\] Ansible Inventory Plugin is missing project filter \[\[\#869\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/869](https\://github\.com/nutanix/nutanix\.ansible/issues/869)\)\]
* ntnx\_prism\_vm\_inventory \- \[Bug\] Inventory Plugin Category Limitation \[\[\#846\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/846](https\://github\.com/nutanix/nutanix\.ansible/issues/846)\)\]
* ntnx\_vms \- \[Bug\] Setting script\_path fails in module ncp\.ntnx\_vms \[\[\#835\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/835](https\://github\.com/nutanix/nutanix\.ansible/issues/835)\)\]
* ntnx\_vms\_v2 \- \[Bug\] Not able to disable apc\_config in module ntnx\_vms\_v2 \[\[\#872\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/872](https\://github\.com/nutanix/nutanix\.ansible/issues/872)\)\]
* website \- \[Bug\] Github page deployment action is failing\. \[\[\#383\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/383](https\://github\.com/nutanix/nutanix\.ansible/issues/383)\)\]

<a id="new-plugins"></a>
### New Plugins

<a id="inventory"></a>
#### Inventory

* nutanix\.ncp\.ntnx\_prism\_host\_inventory\_v2 \- Get a list of Nutanix hosts for ansible dynamic inventory using V4 APIs\.
* nutanix\.ncp\.ntnx\_prism\_vm\_inventory\_v2 \- Get a list of Nutanix VMs for ansible dynamic inventory using V4 APIs\.

<a id="new-modules"></a>
### New Modules

* nutanix\.ncp\.ntnx\_clusters\_categories\_v2 \- Associate or disassociate categories with a Nutanix cluster
* nutanix\.ncp\.ntnx\_clusters\_profile\_association\_v2 \- Associate or disassociate cluster profile with a cluster
* nutanix\.ncp\.ntnx\_clusters\_profiles\_info\_v2 \- Fetch information about clusters profiles in Nutanix Prism Central
* nutanix\.ncp\.ntnx\_clusters\_profiles\_v2 \- Create\, Update and Delete clusters profiles in Nutanix Prism Central
* nutanix\.ncp\.ntnx\_eula\_accept\_v2 \- Accept the EULA for a specific cluster
* nutanix\.ncp\.ntnx\_eula\_info\_v2 \- Fetch information about the EULA for a specific cluster
* nutanix\.ncp\.ntnx\_key\_management\_server\_info\_v2 \- Fetch information about key management server in Nutanix Prism Central
* nutanix\.ncp\.ntnx\_key\_management\_server\_v2 \- Create\, Update and Delete key management server in Nutanix Prism Central
* nutanix\.ncp\.ntnx\_prism\_host\_inventory\_v2 \- Get a list of Nutanix hosts for ansible dynamic inventory
* nutanix\.ncp\.ntnx\_prism\_vm\_inventory\_v2 \- Get a list of Nutanix hosts for ansible dynamic inventory
* nutanix\.ncp\.ntnx\_ssl\_certificates\_info\_v2 \- Fetch information about the SSL certificate for a specific cluster
* nutanix\.ncp\.ntnx\_ssl\_certificates\_v2 \- Update the SSL certificate for a specific cluster
* nutanix\.ncp\.ntnx\_stigs\_info\_v2 \- Get STIGs info in Nutanix Prism Central\.
* nutanix\.ncp\.ntnx\_storage\_policies\_info\_v2 \- Fetch information about storage policies in Nutanix Prism Central
* nutanix\.ncp\.ntnx\_storage\_policies\_v2 \- Create\, Update and Delete storage policies in Nutanix Prism Central

<a id="v2-3-0"></a>
## v2\.3\.0

<a id="release-summary-1"></a>
### Release Summary

Built on v4\.1 SDKs\. Adds OVA management\, Password Managers\, and VM Disk Migration modules with several improvements and bug fixes\.

<a id="minor-changes-1"></a>
### Minor Changes

* All info modules \- \[Imprv\] Enhance Info Modules to Return Total Entities Count for Improved Data Retrieval \[\[\#614\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/614](https\://github\.com/nutanix/nutanix\.ansible/issues/614)\)\]
* All modules \- \[Imprv\] add functionality to disable the state which are not applicable for all the modules \[\[\#746\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/746](https\://github\.com/nutanix/nutanix\.ansible/issues/746)\)\]
* ntnx\_images\_v2 \- \[Imprv\] add complete example playbook for module ntnx\_images\_v2 covering multiple image sources and operations \[\[\#718\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/718](https\://github\.com/nutanix/nutanix\.ansible/issues/718)\)\]
* ntnx\_images\_v2 \- \[Imprv\] add tests for creating images and OVAs using Objects Lite Source \[\[\#717\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/717](https\://github\.com/nutanix/nutanix\.ansible/issues/717)\)\]
* ntnx\_prism\_vm\_inventory \- \[Imprv\] add functionality to be able to set a variable when using module ntnx\_prism\_vm\_inventory \[\[\#644\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/644](https\://github\.com/nutanix/nutanix\.ansible/issues/644)\)\]
* ntnx\_security\_rules\_v2 \- \[Imprv\] add support for additional fields in ntnx\_security\_rules\_v2 \[\[\#719\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/719](https\://github\.com/nutanix/nutanix\.ansible/issues/719)\)\]
* ntnx\_vms\_power\_actions\_v2 \- \[Imprv\] add examples for module ntnx\_vms\_power\_actions\_v2 \[\[\#727\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/727](https\://github\.com/nutanix/nutanix\.ansible/issues/727)\)\]
* ntnx\_vms\_v2 \- \[Imprv\] add automatic cluster selection verification to ntnx\_vms\_v2 tests \[\[\#715\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/715](https\://github\.com/nutanix/nutanix\.ansible/issues/715)\)\]
* ntnx\_vms\_v2 \- \[Imprv\] add functionality to specify project to module ntnx\_vms\_v2 \[\[\#690\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/690](https\://github\.com/nutanix/nutanix\.ansible/issues/690)\)\]
* ntnx\_vms\_v2 \- \[Imprv\] add support for additional fields in nics in ntnx\_vms\_v2 \[\[\#724\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/724](https\://github\.com/nutanix/nutanix\.ansible/issues/724)\)\]
* ntnx\_volume\_groups\_v2 \- \[Feat\] Add update support to ntnx\_volume\_groups\_v2 Ansible module \[\[\#705\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/705](https\://github\.com/nutanix/nutanix\.ansible/issues/705)\)\]
* requirements\.txt \- \[Imprv\] Remove extra python packages from the requirements\.txt file \[\[\#785\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/785](https\://github\.com/nutanix/nutanix\.ansible/issues/785)\)\]

<a id="bugfixes-1"></a>
### Bugfixes

* ntnx\_clusters\_v2 \- \[Bug\] Data type mismatch for categories attribute in module ntnx\_clusters\_v2 \[\[\#759\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/759](https\://github\.com/nutanix/nutanix\.ansible/issues/759)\)\]
* ntnx\_vms\_ngt\_insert\_iso\_v2 \- \[Bug\] How to unmount NGT ISO after install\? \[\[\#739\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/739](https\://github\.com/nutanix/nutanix\.ansible/issues/739)\)\]
* ntnx\_vms\_ngt\_v2 \- \[Bug\] Documentation is incorrect in module ntnx\_vms\_ngt\_v2 \[\[\#693\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/693](https\://github\.com/nutanix/nutanix\.ansible/issues/693)\)\]

<a id="new-modules-1"></a>
### New Modules

* nutanix\.ncp\.ntnx\_ova\_deploy\_vm\_v2 \- Deploy a VM from an OVA in Nutanix Prism Central\.
* nutanix\.ncp\.ntnx\_ova\_download\_v2 \- Download an OVA from Nutanix Prism Central\.
* nutanix\.ncp\.ntnx\_ova\_info\_v2 \- Fetch information about OVA in Nutanix Prism Central\.
* nutanix\.ncp\.ntnx\_ova\_v2 \- Create\, Update and Delete OVA in Nutanix Prism Central\.
* nutanix\.ncp\.ntnx\_password\_managers\_info\_v2 \- Fetch information about Password Managers in Nutanix Prism Central\.
* nutanix\.ncp\.ntnx\_password\_managers\_v2 \- Update Password of System Users in Nutanix Prism Central\.
* nutanix\.ncp\.ntnx\_pc\_task\_abort\_v2 \- Abort a PC Task in Nutanix Prism Central\.
* nutanix\.ncp\.ntnx\_pc\_tasks\_info\_v2 \- Fetch information about PC Tasks in Nutanix Prism Central\.
* nutanix\.ncp\.ntnx\_vms\_disks\_migrate\_v2 \- Migrate disks of a VM in Nutanix Prism Central\.

<a id="v2-2-0"></a>
## v2\.2\.0

<a id="release-summary-2"></a>
### Release Summary

Releasing new modules for Object Stores\, Service Accounts and Several Bugs using PC GA v4\.1 sdks

<a id="minor-changes-2"></a>
### Minor Changes

* Check mode for delete \- \[Imprv\] add functionality check\_mode to module ntnx\_vms \[\[\#334\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/334](https\://github\.com/nutanix/nutanix\.ansible/issues/334)\)\]
* Documentation changes \- \[Imprv\] Add detailed doc for using uuid in modules \[\[\#433\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/433](https\://github\.com/nutanix/nutanix\.ansible/issues/433)\)\]
* ntnx\_prism\_vm\_inventory \- \[Imprv\] Add support for retrieving all VMs without specifying length in inventory plugin \[\[\#651\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/651](https\://github\.com/nutanix/nutanix\.ansible/issues/651)\)\]
* ntnx\_prism\_vm\_inventory \- \[Imprv\] Make changes to include project\_reference in dynamic inventory for groupping \[\[\#500\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/500](https\://github\.com/nutanix/nutanix\.ansible/issues/500)\)\]
* ntnx\_vms\_v2 \- \[Imprv\] add functionality uefi boot\_order to module ntnx\_vms\_v2 \[\[\#579\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/579](https\://github\.com/nutanix/nutanix\.ansible/issues/579)\)\]

<a id="bugfixes-2"></a>
### Bugfixes

* ntnx\_acps \- \[Bug\] Fix comparison of old\_context\_list and update\_context\_list in module ntnx\_acps \[\[\#475\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/475](https\://github\.com/nutanix/nutanix\.ansible/issues/475)\)\]\]
* ntnx\_prism\_vm\_inventory \- \[Bug\] API failure is not in shown while creating dynamic inventory \[\[\#421\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/421](https\://github\.com/nutanix/nutanix\.ansible/issues/421)\)\]
* ntnx\_prism\_vm\_inventory \- \[Bug\] Results of VMs is not more then 500 by default in module inventory \[\[\#354\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/354](https\://github\.com/nutanix/nutanix\.ansible/issues/354)\)\]
* ntnx\_prism\_vm\_inventory \- \[Bug\] galaxy\.ansible doc for ntnx\_prism\_vm\_inventory is having Documentation Syntax Error\. \[\[\#453\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/453](https\://github\.com/nutanix/nutanix\.ansible/issues/453)\)\]
* ntnx\_protection\_rules \- \[Bug\] Fix invalid OU check in user\_groups module \[\[\#481\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/481](https\://github\.com/nutanix/nutanix\.ansible/issues/481)\)\]
* ntnx\_security\_rules \- \[Bug\] Purpose field mandatory to update the security policy from Ansible in module ntnx\_security\_rules \[\[\#485\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/485](https\://github\.com/nutanix/nutanix\.ansible/issues/485)\)\]
* ntnx\_vmm \- \[Bug\] \"not enough positional arguments\" in module plugins/modules/ntnx\_vmy\.py\, line 881 \[\[\#465\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/465](https\://github\.com/nutanix/nutanix\.ansible/issues/465)\)\]
* ntnx\_vms \- \[Bug\] Attaching image to existing disk in module ntnx\_vms \[\[\#454\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/454](https\://github\.com/nutanix/nutanix\.ansible/issues/454)\)\]
* ntnx\_vms \- \[Bug\] Cannot assign IP address on an unmanaged network in module ntnx\_vms \[\[\#593\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/593](https\://github\.com/nutanix/nutanix\.ansible/issues/593)\)\]
* ntnx\_vms\_info\_v2 \- \[Bug\] Can\'t fetch all VMs \[\[\#662\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/662](https\://github\.com/nutanix/nutanix\.ansible/issues/662)\)\]
* ntnx\_vms\_v2 \- \[Bug\] No disk resizing in module ntnx\_vms\_v2 \[\[\#578\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/578](https\://github\.com/nutanix/nutanix\.ansible/issues/578)\)\]
* ntnx\_vms\_v2 \- \[Bug\] state absent does not respect \-\-check mode in module nutanix\_vms \[\[\#534\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/534](https\://github\.com/nutanix/nutanix\.ansible/issues/534)\)\]
* recovery\_plans \- \[Bug\] recovery\_plan fails to create in module plugin\_modules/prism/recovery\_plans\.py \[\[\#515\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/515](https\://github\.com/nutanix/nutanix\.ansible/issues/515)\)\]
* v3 modules \- \[Bug\] \"Failed to convert API response into JSON\" in all modules of Nutanix\.ncp ansible collection \[\[\#490\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/490](https\://github\.com/nutanix/nutanix\.ansible/issues/490)\)\]

<a id="new-modules-2"></a>
### New Modules

* nutanix\.ncp\.ntnx\_object\_stores\_certificate\_info\_v2 \- Fetch information about object stores certificates in Nutanix Prism Central\.
* nutanix\.ncp\.ntnx\_object\_stores\_certificate\_v2 \- Create\, Update and Delete object stores certificates in Nutanix Prism Central\.
* nutanix\.ncp\.ntnx\_object\_stores\_info\_v2 \- Fetch information about object stores in Nutanix Prism Central\.
* nutanix\.ncp\.ntnx\_object\_stores\_v2 \- Create\, Update and Delete object stores in Nutanix Prism Central\.
* nutanix\.ncp\.ntnx\_users\_api\_key\_info\_v2 \- Fetch API key information for a Service account user in Nutanix Prism Central\.
* nutanix\.ncp\.ntnx\_users\_api\_key\_v2 \- Generate or Delete API key for a Service account user in Nutanix Prism Central\.
* nutanix\.ncp\.ntnx\_users\_revoke\_api\_key\_v2 \- Revoke API key for a Service account user in Nutanix Prism Central\.
* nutanix\.ncp\.ntnx\_users\_v2 \- Create Service account in Nutanix Prism Central using ntnx\_users\_v2 module\.

<a id="v2-1-1"></a>
## v2\.1\.1

<a id="release-summary-3"></a>
### Release Summary

Releasing this to make it inline with guidelines of Redhat by removing version cap or fixed version from requirements\.txt

<a id="bugfixes-3"></a>
### Bugfixes

* requirements file \- \[Bug\] The entries in the requirements file MUST NOT have a version cap or be fixed \[\[\#631\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/631](https\://github\.com/nutanix/nutanix\.ansible/issues/631)\)\]

<a id="v2-1-0"></a>
## v2\.1\.0

<a id="release-summary-4"></a>
### Release Summary

Releasing new modules for Prism\, Data Protection\, Data Policies\, LCM and Volumes using PC GA v4 sdks

<a id="breaking-changes--porting-guide-1"></a>
### Breaking Changes / Porting Guide

* nutanix\.ncp collection \- We are deprecating support for ansible\-core\=\=2\.15\.0 and minimum version to use this collection is ansible\-core\=\=2\.16\.0\.

<a id="new-modules-3"></a>
### New Modules

* nutanix\.ncp\.ntnx\_lcm\_config\_info\_v2 \- Fetch LCM Configuration
* nutanix\.ncp\.ntnx\_lcm\_config\_v2 \- Update LCM Configuration
* nutanix\.ncp\.ntnx\_lcm\_entities\_info\_v2 \- Fetch LCM Entities Info
* nutanix\.ncp\.ntnx\_lcm\_inventory\_v2 \- Perform Inventory
* nutanix\.ncp\.ntnx\_lcm\_prechecks\_v2 \- Perform LCM Prechecks
* nutanix\.ncp\.ntnx\_lcm\_status\_info\_v2 \- Get the LCM framework status\.
* nutanix\.ncp\.ntnx\_lcm\_upgrades\_v2 \- Perform LCM upgrades
* nutanix\.ncp\.ntnx\_pc\_backup\_target\_info\_v2 \- Get PC backup targets info
* nutanix\.ncp\.ntnx\_pc\_backup\_target\_v2 \- Create\, Update and Delete a PC backup target\.
* nutanix\.ncp\.ntnx\_pc\_config\_info\_v2 \- Get PC Configuration info
* nutanix\.ncp\.ntnx\_pc\_deploy\_v2 \- Deploys a Prism Central using the provided details
* nutanix\.ncp\.ntnx\_pc\_restorable\_domain\_managers\_info\_v2 \- Fetch restorable domain managers info
* nutanix\.ncp\.ntnx\_pc\_restore\_points\_info\_v2 \- Fetch pc restore points info
* nutanix\.ncp\.ntnx\_pc\_restore\_source\_info\_v2 \- Get PC restore source info
* nutanix\.ncp\.ntnx\_pc\_restore\_source\_v2 \- Creates or Deletes a restore source pointing to a cluster or object store to restore the domain manager\.
* nutanix\.ncp\.ntnx\_pc\_restore\_v2 \- Restores a domain manager\(PC\) from a cluster or object store backup location based on the selected restore point\.
* nutanix\.ncp\.ntnx\_pc\_unregistration\_v2 \- Unregister a PC\-PC setup connected using availability zone\.
* nutanix\.ncp\.ntnx\_promote\_protected\_resources\_v2 \- Module to promote a protected resource in Nutanix Prism Central\.
* nutanix\.ncp\.ntnx\_protected\_resources\_info\_v2 \- Module to fetch protected resource in Nutanix Prism Central\.
* nutanix\.ncp\.ntnx\_protection\_policies\_info\_v2 \- Fetch protection policies info in Nutanix Prism Central
* nutanix\.ncp\.ntnx\_protection\_policies\_v2 \- Create\, Update\, Delete protection policy in Nutanix Prism Central
* nutanix\.ncp\.ntnx\_restore\_protected\_resources\_v2 \- Module to restore a protected resource in Nutanix Prism Central\.
* nutanix\.ncp\.ntnx\_volume\_groups\_categories\_v2 \- Module to associate or disassociate categories with a volume group in Nutanix Prism Central\.

<a id="v2-0-0"></a>
## v2\.0\.0

<a id="release-summary-5"></a>
### Release Summary

Releasing new modules using PC GA v4 sdks

<a id="new-modules-4"></a>
### New Modules

* nutanix\.ncp\.ntnx\_address\_groups\_info\_v2 \- Get address groups info
* nutanix\.ncp\.ntnx\_address\_groups\_v2 \- Create\, Update\, Delete address groups
* nutanix\.ncp\.ntnx\_authorization\_policies\_info\_v2 \- Fetch Authorization policies info from Nutanix PC\.
* nutanix\.ncp\.ntnx\_authorization\_policies\_v2 \- Manage Nutanix PC IAM authorization policies
* nutanix\.ncp\.ntnx\_categories\_info\_v2 \- Nutanix PC categories info module
* nutanix\.ncp\.ntnx\_categories\_v2 \- Manage categories in Nutanix Prism Central
* nutanix\.ncp\.ntnx\_clusters\_info\_v2 \- Retrieve information about Nutanix clusters from PC
* nutanix\.ncp\.ntnx\_clusters\_nodes\_v2 \- Add or Remove nodes from cluster using Nutanix PC
* nutanix\.ncp\.ntnx\_clusters\_v2 \- Manage Nutanix clusters in Prism Central
* nutanix\.ncp\.ntnx\_directory\_services\_info\_v2 \- Fetch directory services info
* nutanix\.ncp\.ntnx\_directory\_services\_v2 \- Module to create\, update and delete directory services in Nutanix PC\.
* nutanix\.ncp\.ntnx\_discover\_unconfigured\_nodes\_v2 \- Discover unconfigured nodes from Nutanix Prism Central
* nutanix\.ncp\.ntnx\_floating\_ips\_info\_v2 \- floating\_ip info module
* nutanix\.ncp\.ntnx\_floating\_ips\_v2 \- floating\_ips module which supports floating\_ip CRUD operations
* nutanix\.ncp\.ntnx\_hosts\_info\_v2 \- Retrieve information about Nutanix hosts from PC\.
* nutanix\.ncp\.ntnx\_image\_placement\_policies\_info\_v2 \- Fetches information about Nutanix PC image placement policies\.
* nutanix\.ncp\.ntnx\_image\_placement\_policies\_v2 \- Manage image placement policies in Nutanix Prism Central
* nutanix\.ncp\.ntnx\_images\_info\_v2 \- Fetch information about Nutanix images
* nutanix\.ncp\.ntnx\_images\_v2 \- Manage Nutanix Prism Central images\.
* nutanix\.ncp\.ntnx\_nodes\_network\_info\_v2 \- Get network information for unconfigured cluster nodes
* nutanix\.ncp\.ntnx\_operations\_info\_v2 \- Module to fetch IAM operations info \(previously <em class="title-reference">permissions</em>\)
* nutanix\.ncp\.ntnx\_pbrs\_info\_v2 \- Routing Policies info module
* nutanix\.ncp\.ntnx\_pbrs\_v2 \- Module for create\, update and delete of Policy based routing\.
* nutanix\.ncp\.ntnx\_pc\_registration\_v2 \- Registers a domain manager \(Prism Central\) instance to other entities like PE and PC
* nutanix\.ncp\.ntnx\_recovery\_point\_replicate\_v2 \- Replicate recovery points
* nutanix\.ncp\.ntnx\_recovery\_point\_restore\_v2 \- Restore recovery points\, Creates a clone of the VM/VG from the selected recovery point
* nutanix\.ncp\.ntnx\_recovery\_points\_info\_v2 \- Get recovery points info
* nutanix\.ncp\.ntnx\_recovery\_points\_v2 \- Create\, Update\, Delete  recovery points
* nutanix\.ncp\.ntnx\_roles\_info\_v2 \- Get roles info
* nutanix\.ncp\.ntnx\_roles\_v2 \- Create\, update\, and delete roles\.
* nutanix\.ncp\.ntnx\_route\_tables\_info\_v2 \- Route tables info module
* nutanix\.ncp\.ntnx\_routes\_info\_v2 \- Routes info module
* nutanix\.ncp\.ntnx\_routes\_v2 \- Module to create\, update\, and delete routes in route table in VPC
* nutanix\.ncp\.ntnx\_saml\_identity\_providers\_info\_v2 \- Fetch SAML identity providers from Nutanix PC
* nutanix\.ncp\.ntnx\_saml\_identity\_providers\_v2 \- Manage SAML identity providers in Nutanix PC
* nutanix\.ncp\.ntnx\_security\_rules\_info\_v2 \- Fetch network security policies info from Nutanix PC\.
* nutanix\.ncp\.ntnx\_security\_rules\_v2 \- Manage network security policies in Nutanix Prism Central
* nutanix\.ncp\.ntnx\_service\_groups\_info\_v2 \- service\_group info module
* nutanix\.ncp\.ntnx\_service\_groups\_v2 \- Create\, Update\, Delete service groups
* nutanix\.ncp\.ntnx\_storage\_containers\_info\_v2 \- Retrieve information about Nutanix storage container from PC
* nutanix\.ncp\.ntnx\_storage\_containers\_stats\_v2 \- Retrieve stats about Nutanix storage container from PC
* nutanix\.ncp\.ntnx\_storage\_containers\_v2 \- Manage storage containers in Nutanix Prism Central
* nutanix\.ncp\.ntnx\_subnets\_info\_v2 \- subnet info module
* nutanix\.ncp\.ntnx\_subnets\_v2 \- subnets module which supports Create\, Update\, Delete subnets
* nutanix\.ncp\.ntnx\_templates\_deploy\_v2 \- Deploy Nutanix templates
* nutanix\.ncp\.ntnx\_templates\_guest\_os\_v2 \- Manage guest OS updates for Nutanix AHV templates\.
* nutanix\.ncp\.ntnx\_templates\_info\_v2 \- template info module
* nutanix\.ncp\.ntnx\_templates\_v2 \- Manage Nutanix AHV template resources
* nutanix\.ncp\.ntnx\_templates\_version\_v2 \- Manage Nutanix template versions
* nutanix\.ncp\.ntnx\_templates\_versions\_info\_v2 \- Fetches information about Nutanix template versions\.
* nutanix\.ncp\.ntnx\_user\_groups\_info\_v2 \- Fetch user groups
* nutanix\.ncp\.ntnx\_user\_groups\_v2 \- Create and Delete user groups
* nutanix\.ncp\.ntnx\_users\_info\_v2 \- Get users info
* nutanix\.ncp\.ntnx\_users\_v2 \- Module to create and update users from Nutanix PC\.
* nutanix\.ncp\.ntnx\_vm\_recovery\_point\_info\_v2 \- Get VM recovery point info
* nutanix\.ncp\.ntnx\_vm\_revert\_v2 \- Revert VM from recovery point
* nutanix\.ncp\.ntnx\_vms\_categories\_v2 \- Associate or disassociate categories to a VM in AHV Nutanix\.
* nutanix\.ncp\.ntnx\_vms\_cd\_rom\_info\_v2 \- Fetch information about Nutanix VM\'s CD ROM
* nutanix\.ncp\.ntnx\_vms\_cd\_rom\_iso\_v2 \- Insert or Eject ISO from CD ROM of Nutanix VMs
* nutanix\.ncp\.ntnx\_vms\_cd\_rom\_v2 \- Manage CDROM for Nutanix AHV VMs
* nutanix\.ncp\.ntnx\_vms\_clone\_v2 \- Clone a virtual machine in Nutanix AHV\.
* nutanix\.ncp\.ntnx\_vms\_disks\_info\_v2 \- Fetch information about Nutanix VM\'s disks
* nutanix\.ncp\.ntnx\_vms\_disks\_v2 \- Manage disks for Nutanix AHV VMs
* nutanix\.ncp\.ntnx\_vms\_info\_v2 \- Fetch information about Nutanix AHV based PC VMs
* nutanix\.ncp\.ntnx\_vms\_ngt\_info\_v2 \- Get Nutanix Guest Tools \(NGT\) current config for a virtual machine\.
* nutanix\.ncp\.ntnx\_vms\_ngt\_insert\_iso\_v2 \- Insert Nutanix Guest Tools \(NGT\) ISO into a virtual machine\.
* nutanix\.ncp\.ntnx\_vms\_ngt\_update\_v2 \- Update Nutanix Guest Tools \(NGT\) configuration for a VM\.
* nutanix\.ncp\.ntnx\_vms\_ngt\_upgrade\_v2 \- Upgrade Nutanix Guest Tools on a VM
* nutanix\.ncp\.ntnx\_vms\_ngt\_v2 \- Install or uninstall Nutanix Guest Tools \(NGT\) on a VM\.
* nutanix\.ncp\.ntnx\_vms\_nics\_info\_v2 \- Fetch information about Nutanix VM\'s NICs
* nutanix\.ncp\.ntnx\_vms\_nics\_ip\_v2 \- Assign/Release IP to/from Nutanix VM NICs\.
* nutanix\.ncp\.ntnx\_vms\_nics\_v2 \- Manage NICs of Nutanix VMs
* nutanix\.ncp\.ntnx\_vms\_serial\_port\_info\_v2 \- Fetch information about Nutanix VM\'s serial ports
* nutanix\.ncp\.ntnx\_vms\_serial\_port\_v2 \- VM Serial Port module which supports VM serial port CRUD states
* nutanix\.ncp\.ntnx\_vms\_stage\_guest\_customization\_v2 \- Stage guest customization configuration for a Nutanix VM
* nutanix\.ncp\.ntnx\_vms\_v2 \- Create\, Update and delete VMs in Nutanix AHV based PC
* nutanix\.ncp\.ntnx\_volume\_groups\_disks\_info\_v2 \- Fetch information about Nutanix PC Volume group disks\.
* nutanix\.ncp\.ntnx\_volume\_groups\_disks\_v2 \- Manage Nutanix volume group disks
* nutanix\.ncp\.ntnx\_volume\_groups\_info\_v2 \- Fetch information about Nutanix PC Volume groups\.
* nutanix\.ncp\.ntnx\_volume\_groups\_iscsi\_clients\_info\_v2 \- Fetch ISCSI clients info\.
* nutanix\.ncp\.ntnx\_volume\_groups\_iscsi\_clients\_v2 \- Manage Nutanix volume groups iscsi clients in Nutanix PC\.
* nutanix\.ncp\.ntnx\_volume\_groups\_v2 \- Manage Nutanix volume group in PC
* nutanix\.ncp\.ntnx\_volume\_groups\_vms\_v2 \- Attach/Detach volume group to AHV VMs in Nutanix PC
* nutanix\.ncp\.ntnx\_vpcs\_info\_v2 \- vpc info module
* nutanix\.ncp\.ntnx\_vpcs\_v2 \- vpcs module which supports vpc CRUD operations

<a id="v1-9-2"></a>
## v1\.9\.2

<a id="release-summary-6"></a>
### Release Summary

Deprecating support for ansible\-core less than v2\.15\.0

<a id="breaking-changes--porting-guide-2"></a>
### Breaking Changes / Porting Guide

* nutanix\.ncp collection \- Due to all versions of ansible\-core version less than v2\.15\.0 are EOL\, we are also deprecating support for same and minimum version to use this collection is ansible\-core\=\=2\.15\.0\. \[\[\#479\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/479](https\://github\.com/nutanix/nutanix\.ansible/issues/479)\)\]

<a id="v1-9-1"></a>
## v1\.9\.1

<a id="release-summary-7"></a>
### Release Summary

This release included bug fixes and improvement\.

<a id="minor-changes-3"></a>
### Minor Changes

* docs \- \[Imprv\] add doc regarding running integration tests locally \[\[\#435\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/435](https\://github\.com/nutanix/nutanix\.ansible/issues/435)\)\]
* info modules \- \[Imprv\] add examples for custom\_filter  \[\[\#416\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/416](https\://github\.com/nutanix/nutanix\.ansible/issues/416)\)\]
* ndb clones \- \[Imprv\] Enable database clones and clone refresh using latest snapshot flag \[\[\#391\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/391](https\://github\.com/nutanix/nutanix\.ansible/issues/391)\)\]
* ndb clones \- \[Imprv\] add examples for NDB database clone under examples folder \[\[\#386\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/386](https\://github\.com/nutanix/nutanix\.ansible/issues/386)\)\]
* ntnx\_prism\_vm\_inventory \- Add support for PC Categories \[\[\#405\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/405](https\://github\.com/nutanix/nutanix\.ansible/issues/405)\)\]
* ntnx\_prism\_vm\_inventory \- \[Imprv\] add examples for dynamic inventory using ntnx\_prism\_vm\_inventory  \[\[\#401\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/401](https\://github\.com/nutanix/nutanix\.ansible/issues/401)\)\]
* ntnx\_vms \- \[Imprv\] add possibility to specify / modify vm user ownership and project \[\[\#378\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/378](https\://github\.com/nutanix/nutanix\.ansible/issues/378)\)\]
* ntnx\_vms \- owner association upon vm creation module \[\[\#359\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/359](https\://github\.com/nutanix/nutanix\.ansible/issues/359)\)\]
* ntnx\_vms\_info \- \[Imprv\] add examples with guest customization for module ntnx\_vms \[\[\#395\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/395](https\://github\.com/nutanix/nutanix\.ansible/issues/395)\)\]

<a id="bugfixes-4"></a>
### Bugfixes

* ntnx\_foundation \- \[Bug\] Error when Clusters Block is missing in module ntnx\_foundation \[\[\#397\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/397](https\://github\.com/nutanix/nutanix\.ansible/issues/397)\)\]
* ntnx\_ndb\_time\_machines\_info \- \[Bug\] ntnx\_ndb\_time\_machines\_info not fetching all attributes when name is used for fetching \[\[\#418\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/418](https\://github\.com/nutanix/nutanix\.ansible/issues/418)\)\]
* ntnx\_security\_rules \- Fix Syntax Errors in Create App Security Rule Example \[\[\#394\]\([https\://github\.com/nutanix/nutanix\.ansible/pull/394/files](https\://github\.com/nutanix/nutanix\.ansible/pull/394/files)\)\]
* ntnx\_vms \- \[Bug\] Error when updating size\_gb using the int filter in module ntnx\_vms \[\[\#400\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/400](https\://github\.com/nutanix/nutanix\.ansible/issues/400)\)\]
* ntnx\_vms \- \[Bug\] hard\_poweroff has been moved to state from operation \[\[\#415\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/415](https\://github\.com/nutanix/nutanix\.ansible/issues/415)\)\]
* ntnx\_vms\_clone \- \[Bug\] cannot change boot\_config when cloning in module ntnx\_vms\_clone \[\[\#360\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/359](https\://github\.com/nutanix/nutanix\.ansible/issues/359)\)\]
* website \- \[Bug\] Github page deployment action is failing\. \[\[\#483\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/483](https\://github\.com/nutanix/nutanix\.ansible/issues/483)\)\]

<a id="v1-9-0"></a>
## v1\.9\.0

<a id="minor-changes-4"></a>
### Minor Changes

* ntnx\_profiles\_info \- \[Impr\] Develop ansible module for getting available IPs for given network profiles in NDB \[\#345\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/345](https\://github\.com/nutanix/nutanix\.ansible/issues/345)\)
* ntnx\_security\_rules \- \[Imprv\] Flow Network Security Multi\-Tier support in Security Policy definition \[\#319\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/319](https\://github\.com/nutanix/nutanix\.ansible/issues/319)\)

<a id="deprecated-features"></a>
### Deprecated Features

* ntnx\_security\_rules \- The <code>apptier</code> option in target group has been removed\. New option called <code>apptiers</code> has been added to support multi tier policy\.

<a id="bugfixes-5"></a>
### Bugfixes

* info modules \- \[Bug\] Multiple filters params are not considered for fetching entities in PC based info modules \[\[\#352\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/352](https\://github\.com/nutanix/nutanix\.ansible/issues/352)\)\]
* ntnx\_foundation \- \[Bug\] clusters parameters not being passed to Foundation Server in module nutanix\.ncp\.ntnx\_foundation \[\[\#307\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/307](https\://github\.com/nutanix/nutanix\.ansible/issues/307)\)\]
* ntnx\_karbon\_clusters \- \[Bug\] error in sample karbon/create\_k8s\_cluster\.yml \[\[\#349\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/349](https\://github\.com/nutanix/nutanix\.ansible/issues/349)\)\]
* ntnx\_karbon\_clusters \- \[Bug\] impossible to deploy NKE cluster with etcd using disk smaller than 120GB \[\[\#350\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/350](https\://github\.com/nutanix/nutanix\.ansible/issues/350)\)\]
* ntnx\_subnets \- \[Bug\] wrong virtual\_switch selected in module ntnx\_subnets \[\#328\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/328](https\://github\.com/nutanix/nutanix\.ansible/issues/328)\)

<a id="new-modules-5"></a>
### New Modules

* nutanix\.ncp\.ntnx\_karbon\_clusters\_node\_pools \- Create\,Update and Delete a worker node pools with the provided configuration\.
* nutanix\.ncp\.ntnx\_ndb\_tags\_info \- info module for ndb tags info

<a id="v1-8-0"></a>
## v1\.8\.0

<a id="new-modules-6"></a>
### New Modules

* nutanix\.ncp\.ntnx\_ndb\_authorize\_db\_server\_vms \- module for authorizing db server vm
* nutanix\.ncp\.ntnx\_ndb\_clones\_info \- info module for database clones
* nutanix\.ncp\.ntnx\_ndb\_clusters \- Create\, Update and Delete NDB clusters
* nutanix\.ncp\.ntnx\_ndb\_clusters\_info \- info module for ndb clusters info
* nutanix\.ncp\.ntnx\_ndb\_database\_clone\_refresh \- module for database clone refresh\.
* nutanix\.ncp\.ntnx\_ndb\_database\_clones \- module for create\, update and delete of ndb database clones
* nutanix\.ncp\.ntnx\_ndb\_database\_log\_catchup \- module for performing log catchups action
* nutanix\.ncp\.ntnx\_ndb\_database\_restore \- module for restoring database instance
* nutanix\.ncp\.ntnx\_ndb\_database\_scale \- module for scaling database instance
* nutanix\.ncp\.ntnx\_ndb\_database\_snapshots \- module for creating\, updating and deleting database snapshots
* nutanix\.ncp\.ntnx\_ndb\_databases \- Module for create\, update and delete of single instance database\. Currently\, postgres type database is officially supported\.
* nutanix\.ncp\.ntnx\_ndb\_databases\_info \- info module for ndb database instances
* nutanix\.ncp\.ntnx\_ndb\_db\_server\_vms \- module for create\, delete and update of database server vms
* nutanix\.ncp\.ntnx\_ndb\_db\_servers\_info \- info module for ndb db server vms info
* nutanix\.ncp\.ntnx\_ndb\_linked\_databases \- module to manage linked databases of a database instance
* nutanix\.ncp\.ntnx\_ndb\_maintenance\_tasks \- module to add and remove maintenance related tasks
* nutanix\.ncp\.ntnx\_ndb\_maintenance\_window \- module to create\, update and delete maintenance window
* nutanix\.ncp\.ntnx\_ndb\_maintenance\_windows\_info \- module for fetching maintenance windows info
* nutanix\.ncp\.ntnx\_ndb\_profiles \- module for create\, update and delete of profiles
* nutanix\.ncp\.ntnx\_ndb\_profiles\_info \- info module for ndb profiles
* nutanix\.ncp\.ntnx\_ndb\_register\_database \- module for database instance registration
* nutanix\.ncp\.ntnx\_ndb\_register\_db\_server\_vm \- module for registration of database server vm
* nutanix\.ncp\.ntnx\_ndb\_replicate\_database\_snapshots \- module for replicating database snapshots across clusters of time machine
* nutanix\.ncp\.ntnx\_ndb\_slas \- module for creating\, updating and deleting slas
* nutanix\.ncp\.ntnx\_ndb\_slas\_info \- info module for ndb slas
* nutanix\.ncp\.ntnx\_ndb\_snapshots\_info \- info module for ndb snapshots info
* nutanix\.ncp\.ntnx\_ndb\_stretched\_vlans \- Module for create\, update and delete of stretched vlan\.
* nutanix\.ncp\.ntnx\_ndb\_tags \- module for create\, update and delete of tags
* nutanix\.ncp\.ntnx\_ndb\_time\_machine\_clusters \- Module for create\, update and delete for data access management in time machines\.
* nutanix\.ncp\.ntnx\_ndb\_time\_machines\_info \- info module for ndb time machines
* nutanix\.ncp\.ntnx\_ndb\_vlans \- Module for create\, update and delete of ndb vlan\.
* nutanix\.ncp\.ntnx\_ndb\_vlans\_info \- info module for ndb vlans

<a id="v1-7-0"></a>
## v1\.7\.0

<a id="minor-changes-5"></a>
### Minor Changes

* examples \- \[Imprv\] Add version related notes to examples \[\#279\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/279](https\://github\.com/nutanix/nutanix\.ansible/issues/279)\)
* examples \- \[Imprv\] Fix IaaS example \[\#250\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/250](https\://github\.com/nutanix/nutanix\.ansible/issues/250)\)
* examples \- \[Imprv\] add examples of Images and Static Routes Module \[\#256\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/256](https\://github\.com/nutanix/nutanix\.ansible/issues/256)\)
* ntnx\_projects \- \[Feat\] Add capability to configure role mappings with collaboration on/off in ntnx\_projects \[\#252\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/252](https\://github\.com/nutanix/nutanix\.ansible/issues/252)\)
* ntnx\_projects \- \[Imprv\] add vpcs and overlay subnets configure capability to module ntnx\_projects \[\#289\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/289](https\://github\.com/nutanix/nutanix\.ansible/issues/289)\)
* ntnx\_vms \- \[Imprv\] add functionality to set network mac\_address to module ntnx\_vms \[\#201\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/201](https\://github\.com/nutanix/nutanix\.ansible/issues/201)\)
* nutanix\.ncp\.ntnx\_prism\_vm\_inventory \- \[Imprv\] add functionality constructed to module inventory \[\#235\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/235](https\://github\.com/nutanix/nutanix\.ansible/issues/235)\)

<a id="bugfixes-6"></a>
### Bugfixes

* ntnx\_projects \- \[Bug\] Clusters and subnets configured in project are not visible in new projects UI \[\#283\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/283](https\://github\.com/nutanix/nutanix\.ansible/issues/283)\)
* ntnx\_vms \- Subnet Name \-\-\> UUID Lookup should be PE Cluster Aware \[\#260\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/260](https\://github\.com/nutanix/nutanix\.ansible/issues/260)\)
* nutanix\.ncp\.ntnx\_prism\_vm\_inventory \- \[Bug\] Inventory does not fetch more than 500 Entities \[\[\#228\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/228](https\://github\.com/nutanix/nutanix\.ansible/issues/228)\)\]

<a id="v1-6-0"></a>
## v1\.6\.0

<a id="new-modules-7"></a>
### New Modules

* nutanix\.ncp\.ntnx\_karbon\_clusters \- v4 sdks based module for karbon clusters
* nutanix\.ncp\.ntnx\_karbon\_clusters\_info \- Nutanix info module for karbon clusters with kubeconifg and ssh config
* nutanix\.ncp\.ntnx\_karbon\_registries \- v4 sdks based module for karbon private registry
* nutanix\.ncp\.ntnx\_karbon\_registries\_info \- Nutanix info module for karbon private registry

<a id="v1-5-0"></a>
## v1\.5\.0

<a id="new-modules-8"></a>
### New Modules

* nutanix\.ncp\.ntnx\_protection\_rules \- v4 sdks based module for protection rules
* nutanix\.ncp\.ntnx\_protection\_rules\_info \- Nutanix info module for protection rules
* nutanix\.ncp\.ntnx\_recovery\_plan\_jobs \- v4 sdks based module for recovery plan jobs
* nutanix\.ncp\.ntnx\_recovery\_plan\_jobs\_info \- Nutanix info module for protection
* nutanix\.ncp\.ntnx\_recovery\_plans \- v4 sdks based module for recovery plan
* nutanix\.ncp\.ntnx\_recovery\_plans\_info \- Nutanix info module for recovery plan

<a id="v1-4-0"></a>
## v1\.4\.0

<a id="bugfixes-7"></a>
### Bugfixes

* Fix examples of info modules \[\#226\]\([https\://github\.com/nutanix/nutanix\.ansible/issues/226](https\://github\.com/nutanix/nutanix\.ansible/issues/226)\)

<a id="new-modules-9"></a>
### New Modules

* nutanix\.ncp\.ntnx\_acps \- acp module which suports acp Create\, update and delete operations
* nutanix\.ncp\.ntnx\_acps\_info \- acp info module
* nutanix\.ncp\.ntnx\_address\_groups \- module which supports address groups CRUD operations
* nutanix\.ncp\.ntnx\_address\_groups\_info \- address groups info module
* nutanix\.ncp\.ntnx\_categories \- category module which supports pc category management CRUD operations
* nutanix\.ncp\.ntnx\_categories\_info \- categories info module
* nutanix\.ncp\.ntnx\_clusters\_info \- cluster info module
* nutanix\.ncp\.ntnx\_hosts\_info \- host  info module
* nutanix\.ncp\.ntnx\_permissions\_info \- permissions info module
* nutanix\.ncp\.ntnx\_projects \- module for create\, update and delete pc projects
* nutanix\.ncp\.ntnx\_projects\_info \- projects info module
* nutanix\.ncp\.ntnx\_roles \- module which supports role CRUD operations
* nutanix\.ncp\.ntnx\_roles\_info \- role info module
* nutanix\.ncp\.ntnx\_service\_groups \- service\_groups module which suports service\_groups CRUD operations
* nutanix\.ncp\.ntnx\_service\_groups\_info \- service\_group info module
* nutanix\.ncp\.ntnx\_user\_groups \- user\_groups module which supports pc user\_groups management create delete operations
* nutanix\.ncp\.ntnx\_user\_groups\_info \- User Groups info module
* nutanix\.ncp\.ntnx\_users \- users module which supports pc users management create delete operations
* nutanix\.ncp\.ntnx\_users\_info \- users info module

<a id="v1-3-0"></a>
## v1\.3\.0

<a id="new-modules-10"></a>
### New Modules

* nutanix\.ncp\.ntnx\_image\_placement\_policies\_info \- image placement policies info module
* nutanix\.ncp\.ntnx\_image\_placement\_policy \- image placement policy module which supports Create\, update and delete operations
* nutanix\.ncp\.ntnx\_images \- images module which supports pc images management CRUD operations
* nutanix\.ncp\.ntnx\_images\_info \- images info module
* nutanix\.ncp\.ntnx\_security\_rules \- security\_rule module which suports security\_rule CRUD operations
* nutanix\.ncp\.ntnx\_security\_rules\_info \- security\_rule info module
* nutanix\.ncp\.ntnx\_static\_routes \- vpc static routes
* nutanix\.ncp\.ntnx\_static\_routes\_info \- vpc static routes info module

<a id="v1-2-0"></a>
## v1\.2\.0

<a id="minor-changes-6"></a>
### Minor Changes

* VM\'s update functionality

<a id="new-modules-11"></a>
### New Modules

* nutanix\.ncp\.ntnx\_floating\_ips\_info \- Nutanix info module for floating Ips
* nutanix\.ncp\.ntnx\_pbrs\_info \- Nutanix info module for policy based routing
* nutanix\.ncp\.ntnx\_subnets\_info \- Nutanix info module for subnets
* nutanix\.ncp\.ntnx\_vms\_clone \- VM module which supports VM clone operations
* nutanix\.ncp\.ntnx\_vms\_info \- Nutanix info module for vms
* nutanix\.ncp\.ntnx\_vms\_ova \- VM module which supports ova creation
* nutanix\.ncp\.ntnx\_vpcs\_info \- Nutanix info module for vpcs

<a id="v1-1-0"></a>
## v1\.1\.0

<a id="minor-changes-7"></a>
### Minor Changes

* Added integration tests for foundation and foundation central

<a id="new-modules-12"></a>
### New Modules

* nutanix\.ncp\.ntnx\_foundation \- Nutanix module to image nodes and optionally create clusters
* nutanix\.ncp\.ntnx\_foundation\_bmc\_ipmi\_config \- Nutanix module which configures IPMI IP address on BMC of nodes\.
* nutanix\.ncp\.ntnx\_foundation\_central \- Nutanix module to imaged Nodes and optionally create cluster
* nutanix\.ncp\.ntnx\_foundation\_central\_api\_keys \- Nutanix module which creates api key for foundation central
* nutanix\.ncp\.ntnx\_foundation\_central\_api\_keys\_info \- Nutanix module which returns the api key
* nutanix\.ncp\.ntnx\_foundation\_central\_imaged\_clusters\_info \- Nutanix module which returns the imaged clusters within the Foundation Central
* nutanix\.ncp\.ntnx\_foundation\_central\_imaged\_nodes\_info \- Nutanix module which returns the imaged nodes within the Foundation Central
* nutanix\.ncp\.ntnx\_foundation\_discover\_nodes\_info \- Nutanix module which returns nodes discovered by Foundation
* nutanix\.ncp\.ntnx\_foundation\_hypervisor\_images\_info \- Nutanix module which returns the hypervisor images uploaded to Foundation
* nutanix\.ncp\.ntnx\_foundation\_image\_upload \- Nutanix module which uploads hypervisor or AOS image to foundation vm\.
* nutanix\.ncp\.ntnx\_foundation\_node\_network\_info \- Nutanix module which returns node network information discovered by Foundation

<a id="v1-0-0"></a>
## v1\.0\.0

<a id="major-changes"></a>
### Major Changes

* CICD pipeline using GitHub actions

<a id="minor-changes-8"></a>
### Minor Changes

* Add meta file for collection
* Allow environment variables for nutanix connection parameters
* Codegen \- Ansible code generator
* Imprv cluster uuid \[\#75\]\([https\://github\.com/nutanix/nutanix\.ansible/pull/75](https\://github\.com/nutanix/nutanix\.ansible/pull/75)\)
* Imprv/code coverage \[\#97\]\([https\://github\.com/nutanix/nutanix\.ansible/pull/97](https\://github\.com/nutanix/nutanix\.ansible/pull/97)\)
* Imprv/vpcs network prefix \[\#81\]\([https\://github\.com/nutanix/nutanix\.ansible/pull/81](https\://github\.com/nutanix/nutanix\.ansible/pull/81)\)

<a id="bugfixes-8"></a>
### Bugfixes

* Bug/cluster UUID issue68 \[\#72\]\([https\://github\.com/nutanix/nutanix\.ansible/pull/72](https\://github\.com/nutanix/nutanix\.ansible/pull/72)\)
* Client SDK with inventory \[\#45\]\([https\://github\.com/nutanix/nutanix\.ansible/pull/45](https\://github\.com/nutanix/nutanix\.ansible/pull/45)\)
* Creating a VM based on a disk\_image without specifying the size\_gb
* Fix error messages for get\_uuid\(\) reponse \[\#47\]\([https\://github\.com/nutanix/nutanix\.ansible/pull/47](https\://github\.com/nutanix/nutanix\.ansible/pull/47)\)
* Fix/integ \[\#96\]\([https\://github\.com/nutanix/nutanix\.ansible/pull/96](https\://github\.com/nutanix/nutanix\.ansible/pull/96)\)
* Sanity and python fix \[\#46\]\([https\://github\.com/nutanix/nutanix\.ansible/pull/46](https\://github\.com/nutanix/nutanix\.ansible/pull/46)\)
* Task/fix failing sanity \[\#117\]\([https\://github\.com/nutanix/nutanix\.ansible/pull/117](https\://github\.com/nutanix/nutanix\.ansible/pull/117)\)
* black fixes \[\#30\]\([https\://github\.com/nutanix/nutanix\.ansible/pull/30](https\://github\.com/nutanix/nutanix\.ansible/pull/30)\)
* black fixes \[\#32\]\([https\://github\.com/nutanix/nutanix\.ansible/pull/32](https\://github\.com/nutanix/nutanix\.ansible/pull/32)\)
* clean up pbrs\.py \[\#113\]\([https\://github\.com/nutanix/nutanix\.ansible/pull/113](https\://github\.com/nutanix/nutanix\.ansible/pull/113)\)
* clear unused files and argument \[\#29\]\([https\://github\.com/nutanix/nutanix\.ansible/pull/29](https\://github\.com/nutanix/nutanix\.ansible/pull/29)\)
* code cleanup \- fix github issue\#59 \[\#60\]\([https\://github\.com/nutanix/nutanix\.ansible/pull/60](https\://github\.com/nutanix/nutanix\.ansible/pull/60)\)
* device index calculation fixes\, updates for get by name functionality\[\#254\]\([https\://github\.com/nutanix/nutanix\.ansible/pull/42](https\://github\.com/nutanix/nutanix\.ansible/pull/42)\)
* fix project name \[\#107\]\([https\://github\.com/nutanix/nutanix\.ansible/pull/107](https\://github\.com/nutanix/nutanix\.ansible/pull/107)\)
* fixed variables names issue74 \[\#77\]\([https\://github\.com/nutanix/nutanix\.ansible/pull/77](https\://github\.com/nutanix/nutanix\.ansible/pull/77)\)
* fixes to get spec from collection \[\#17\]\([https\://github\.com/nutanix/nutanix\.ansible/pull/17](https\://github\.com/nutanix/nutanix\.ansible/pull/17)\)
* icmp \"any\" code value in module PBR
* solve python 2\.7 issues \[\#41\]\([https\://github\.com/nutanix/nutanix\.ansible/pull/41](https\://github\.com/nutanix/nutanix\.ansible/pull/41)\)
* updates for guest customization spec \[\#20\]\([https\://github\.com/nutanix/nutanix\.ansible/pull/20](https\://github\.com/nutanix/nutanix\.ansible/pull/20)\)

<a id="new-modules-13"></a>
### New Modules

* nutanix\.ncp\.ntnx\_floating\_ips \- v4 sdks based module for floating Ips
* nutanix\.ncp\.ntnx\_pbrs \- v4 sdks based module for policy based routing
* nutanix\.ncp\.ntnx\_subnets \- v4 sdks based module for subnets
* nutanix\.ncp\.ntnx\_vms \- v4 sdks based module for vms
* nutanix\.ncp\.ntnx\_vpcs \- v4 sdks based module for vpcs
