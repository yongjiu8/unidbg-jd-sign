package com.spider.unidbgserver.configuration;

import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.DalvikModule;
import com.github.unidbg.linux.android.dvm.VM;
import com.github.unidbg.memory.Memory;
import com.spider.unidbgserver.jni.JDJni;
import com.spider.unidbgserver.vm.JDVm;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.ClassPathResource;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;

@Configuration
public class JDConfiguration {

    public static String pkgName = "com.jingdong.app.mall";
    @Value("${apk.path}")
    public String apkPath;
    @Value("${so.path}")
    public String soPath;

    @Bean(name = "jdVm")
    public JDVm jdVm() throws IOException {
        JDVm jdVm = new JDVm();

        AndroidEmulator emulator = AndroidEmulatorBuilder.for32Bit().setProcessName(pkgName).build();
        final Memory memory = emulator.getMemory();
        memory.setLibraryResolver(new AndroidResolver(23));
        VM vm = emulator.createDalvikVM(new File(apkPath));
        vm.setJni(new JDJni());
        jdVm.setEmulator(emulator);
        jdVm.setVm(vm);
        return jdVm;
    }

    @Bean("jdModule")
    public DalvikModule jdModule(@Qualifier("jdVm") JDVm jdVm) throws IOException {
        VM vm = jdVm.getVm();

        AndroidEmulator emulator = jdVm.getEmulator();
        DalvikModule dm = vm.loadLibrary(new File(soPath), false);
        vm.setVerbose(true);
        dm.callJNI_OnLoad(emulator);
        return dm;
    }

}
