/* Generated code for Python module 'oauthlib.oauth2.rfc6749.request_validator'
 * created by Nuitka version 1.5.3
 *
 * This code is in part copyright 2022 Kay Hayen.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "nuitka/prelude.h"

#include "nuitka/unfreezing.h"

#include "__helpers.h"

/* The "module_oauthlib$oauth2$rfc6749$request_validator" is a Python object pointer of module type.
 *
 * Note: For full compatibility with CPython, every module variable access
 * needs to go through it except for cases where the module cannot possibly
 * have changed in the mean time.
 */

PyObject *module_oauthlib$oauth2$rfc6749$request_validator;
PyDictObject *moduledict_oauthlib$oauth2$rfc6749$request_validator;

/* The declarations of module constants used, if any. */
static PyObject *mod_consts[125];
#ifndef __NUITKA_NO_ASSERT__
static Py_hash_t mod_consts_hash[125];
#endif

static PyObject *module_filename_obj = NULL;

/* Indicator if this modules private constants were created yet. */
static bool constants_created = false;

/* Function to create module private constants. */
static void createModuleConstants(void) {
    if (constants_created == false) {
        loadConstantsBlob(&mod_consts[0], UNTRANSLATE("oauthlib.oauth2.rfc6749.request_validator"));
        constants_created = true;

#ifndef __NUITKA_NO_ASSERT__
        for (int i = 0; i < 125; i++) {
            mod_consts_hash[i] = DEEP_HASH(mod_consts[i]);
        }
#endif
    }
}

// We want to be able to initialize the "__main__" constants in any case.
#if 0
void createMainModuleConstants(void) {
    createModuleConstants();
}
#endif

/* Function to verify module private constants for non-corruption. */
#ifndef __NUITKA_NO_ASSERT__
void checkModuleConstants_oauthlib$oauth2$rfc6749$request_validator(void) {
    // The module may not have been used at all, then ignore this.
    if (constants_created == false) return;

    for (int i = 0; i < 125; i++) {
        assert(mod_consts_hash[i] == DEEP_HASH(mod_consts[i]));
        CHECK_OBJECT_DEEP(mod_consts[i]);
    }
}
#endif

// The module code objects.
static PyCodeObject *codeobj_798142724311027663b78add05f0a5d9;
static PyCodeObject *codeobj_cb20c4dfbed080a14a85811f41839e22;
static PyCodeObject *codeobj_176cec46e6b5ee76aee1ea4e54060d30;
static PyCodeObject *codeobj_e9ca277b71c24aad2da879e1094a443c;
static PyCodeObject *codeobj_2a16f0793529ed9c7bae140e1ea16ad2;
static PyCodeObject *codeobj_15868616fd3d30e52f339280b08667d6;
static PyCodeObject *codeobj_ba068dbaf8b68cb9c006b9ee06af5e58;
static PyCodeObject *codeobj_dfb0755ba293c104853cc61335c50977;
static PyCodeObject *codeobj_41a3ece1a35709f73a6c917b7c80bf46;
static PyCodeObject *codeobj_17f5e2b7f4eac3a3190f4cbbed334286;
static PyCodeObject *codeobj_f2c4f529262545335009559750e8e70e;
static PyCodeObject *codeobj_eb455e7e8b0726ab205bddb0b5032af7;
static PyCodeObject *codeobj_fca600ed8fd6b12437c84c1597335333;
static PyCodeObject *codeobj_67cb4221245cb811c4d7b534a6497083;
static PyCodeObject *codeobj_590a91faa164b246a361eec1a702b5e4;
static PyCodeObject *codeobj_88f698014760404e5103d09728eed55f;
static PyCodeObject *codeobj_23a6ed71221ed055494325ccce6c7aff;
static PyCodeObject *codeobj_a60172c1215f2f00cf0915196d66e963;
static PyCodeObject *codeobj_30c9aaa654910caf6b84f64746df29d8;
static PyCodeObject *codeobj_f6577c7b7854260253ce470c8440f149;
static PyCodeObject *codeobj_4ab337411e6dd7f76096474107aada62;
static PyCodeObject *codeobj_538ba625ac81714084cc16afd96934c9;
static PyCodeObject *codeobj_22929cfc4badf0d11a356027b016beba;
static PyCodeObject *codeobj_770e7fbf1d2d8bd6051ac5649e1d0dc2;
static PyCodeObject *codeobj_b3675bb61cf0f9b19c800807c4973f4b;
static PyCodeObject *codeobj_3e7b33e54320d6baa5b70180221efaf4;
static PyCodeObject *codeobj_35e4dba3786838d11c6792c05107d109;
static PyCodeObject *codeobj_489b9d905bb815d7f1578d1548e010e5;
static PyCodeObject *codeobj_99168fe18391008f5fa4fc4155dd7815;

static void createModuleCodeObjects(void) {
    module_filename_obj = MAKE_RELATIVE_PATH(mod_consts[102]); CHECK_OBJECT(module_filename_obj);
    codeobj_798142724311027663b78add05f0a5d9 = MAKE_CODE_OBJECT(module_filename_obj, 1, CO_NOFREE, mod_consts[103], mod_consts[103], NULL, NULL, 0, 0, 0);
    codeobj_cb20c4dfbed080a14a85811f41839e22 = MAKE_CODE_OBJECT(module_filename_obj, 41, CO_OPTIMIZED | CO_NEWLOCALS | CO_VARARGS | CO_VARKEYWORDS | CO_NOFREE, mod_consts[43], mod_consts[43], mod_consts[104], NULL, 2, 0, 0);
    codeobj_176cec46e6b5ee76aee1ea4e54060d30 = MAKE_CODE_OBJECT(module_filename_obj, 77, CO_OPTIMIZED | CO_NEWLOCALS | CO_VARARGS | CO_VARKEYWORDS | CO_NOFREE, mod_consts[45], mod_consts[45], mod_consts[105], NULL, 3, 0, 0);
    codeobj_e9ca277b71c24aad2da879e1094a443c = MAKE_CODE_OBJECT(module_filename_obj, 12, CO_OPTIMIZED | CO_NEWLOCALS | CO_VARARGS | CO_VARKEYWORDS | CO_NOFREE, mod_consts[41], mod_consts[41], mod_consts[104], NULL, 2, 0, 0);
    codeobj_2a16f0793529ed9c7bae140e1ea16ad2 = MAKE_CODE_OBJECT(module_filename_obj, 97, CO_OPTIMIZED | CO_NEWLOCALS | CO_VARARGS | CO_VARKEYWORDS | CO_NOFREE, mod_consts[47], mod_consts[47], mod_consts[106], NULL, 6, 0, 0);
    codeobj_15868616fd3d30e52f339280b08667d6 = MAKE_CODE_OBJECT(module_filename_obj, 607, CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE, mod_consts[94], mod_consts[94], mod_consts[107], NULL, 3, 0, 0);
    codeobj_ba068dbaf8b68cb9c006b9ee06af5e58 = MAKE_CODE_OBJECT(module_filename_obj, 636, CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE, mod_consts[96], mod_consts[96], mod_consts[107], NULL, 3, 0, 0);
    codeobj_dfb0755ba293c104853cc61335c50977 = MAKE_CODE_OBJECT(module_filename_obj, 121, CO_OPTIMIZED | CO_NEWLOCALS | CO_VARARGS | CO_VARKEYWORDS | CO_NOFREE, mod_consts[49], mod_consts[49], mod_consts[105], NULL, 3, 0, 0);
    codeobj_41a3ece1a35709f73a6c917b7c80bf46 = MAKE_CODE_OBJECT(module_filename_obj, 135, CO_OPTIMIZED | CO_NEWLOCALS | CO_VARARGS | CO_VARKEYWORDS | CO_NOFREE, mod_consts[51], mod_consts[51], mod_consts[105], NULL, 3, 0, 0);
    codeobj_17f5e2b7f4eac3a3190f4cbbed334286 = MAKE_CODE_OBJECT(module_filename_obj, 151, CO_OPTIMIZED | CO_NEWLOCALS | CO_VARARGS | CO_VARKEYWORDS | CO_NOFREE, mod_consts[53], mod_consts[53], mod_consts[108], NULL, 3, 0, 0);
    codeobj_f2c4f529262545335009559750e8e70e = MAKE_CODE_OBJECT(module_filename_obj, 186, CO_OPTIMIZED | CO_NEWLOCALS | CO_VARARGS | CO_VARKEYWORDS | CO_NOFREE, mod_consts[58], mod_consts[58], mod_consts[109], NULL, 4, 0, 0);
    codeobj_eb455e7e8b0726ab205bddb0b5032af7 = MAKE_CODE_OBJECT(module_filename_obj, 228, CO_OPTIMIZED | CO_NEWLOCALS | CO_VARARGS | CO_VARKEYWORDS | CO_NOFREE, mod_consts[60], mod_consts[60], mod_consts[110], NULL, 4, 0, 0);
    codeobj_fca600ed8fd6b12437c84c1597335333 = MAKE_CODE_OBJECT(module_filename_obj, 656, CO_OPTIMIZED | CO_NEWLOCALS | CO_VARARGS | CO_VARKEYWORDS | CO_NOFREE, mod_consts[99], mod_consts[99], mod_consts[111], NULL, 4, 0, 0);
    codeobj_67cb4221245cb811c4d7b534a6497083 = MAKE_CODE_OBJECT(module_filename_obj, 581, CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE, mod_consts[91], mod_consts[91], mod_consts[112], NULL, 3, 0, 0);
    codeobj_590a91faa164b246a361eec1a702b5e4 = MAKE_CODE_OBJECT(module_filename_obj, 164, CO_OPTIMIZED | CO_NEWLOCALS | CO_VARARGS | CO_VARKEYWORDS | CO_NOFREE, mod_consts[56], mod_consts[56], mod_consts[113], NULL, 4, 0, 0);
    codeobj_88f698014760404e5103d09728eed55f = MAKE_CODE_OBJECT(module_filename_obj, 241, CO_OPTIMIZED | CO_NEWLOCALS | CO_VARARGS | CO_VARKEYWORDS | CO_NOFREE, mod_consts[62], mod_consts[62], mod_consts[109], NULL, 4, 0, 0);
    codeobj_23a6ed71221ed055494325ccce6c7aff = MAKE_CODE_OBJECT(module_filename_obj, 254, CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE, mod_consts[65], mod_consts[65], mod_consts[114], NULL, 2, 0, 0);
    codeobj_a60172c1215f2f00cf0915196d66e963 = MAKE_CODE_OBJECT(module_filename_obj, 270, CO_OPTIMIZED | CO_NEWLOCALS | CO_VARARGS | CO_VARKEYWORDS | CO_NOFREE, mod_consts[67], mod_consts[67], mod_consts[110], NULL, 4, 0, 0);
    codeobj_30c9aaa654910caf6b84f64746df29d8 = MAKE_CODE_OBJECT(module_filename_obj, 317, CO_OPTIMIZED | CO_NEWLOCALS | CO_VARARGS | CO_VARKEYWORDS | CO_NOFREE, mod_consts[11], mod_consts[11], mod_consts[115], NULL, 3, 0, 0);
    codeobj_f6577c7b7854260253ce470c8440f149 = MAKE_CODE_OBJECT(module_filename_obj, 306, CO_OPTIMIZED | CO_NEWLOCALS | CO_VARARGS | CO_VARKEYWORDS | CO_NOFREE, mod_consts[69], mod_consts[69], mod_consts[115], NULL, 3, 0, 0);
    codeobj_4ab337411e6dd7f76096474107aada62 = MAKE_CODE_OBJECT(module_filename_obj, 367, CO_OPTIMIZED | CO_NEWLOCALS | CO_NOFREE, mod_consts[72], mod_consts[72], mod_consts[116], NULL, 4, 0, 0);
    codeobj_538ba625ac81714084cc16afd96934c9 = MAKE_CODE_OBJECT(module_filename_obj, 419, CO_OPTIMIZED | CO_NEWLOCALS | CO_VARARGS | CO_VARKEYWORDS | CO_NOFREE, mod_consts[74], mod_consts[74], mod_consts[105], NULL, 3, 0, 0);
    codeobj_22929cfc4badf0d11a356027b016beba = MAKE_CODE_OBJECT(module_filename_obj, 437, CO_OPTIMIZED | CO_NEWLOCALS | CO_VARARGS | CO_VARKEYWORDS | CO_NOFREE, mod_consts[76], mod_consts[76], mod_consts[117], NULL, 5, 0, 0);
    codeobj_770e7fbf1d2d8bd6051ac5649e1d0dc2 = MAKE_CODE_OBJECT(module_filename_obj, 472, CO_OPTIMIZED | CO_NEWLOCALS | CO_VARARGS | CO_VARKEYWORDS | CO_NOFREE, mod_consts[78], mod_consts[78], mod_consts[118], NULL, 5, 0, 0);
    codeobj_b3675bb61cf0f9b19c800807c4973f4b = MAKE_CODE_OBJECT(module_filename_obj, 490, CO_OPTIMIZED | CO_NEWLOCALS | CO_VARARGS | CO_VARKEYWORDS | CO_NOFREE, mod_consts[80], mod_consts[80], mod_consts[119], NULL, 4, 0, 0);
    codeobj_3e7b33e54320d6baa5b70180221efaf4 = MAKE_CODE_OBJECT(module_filename_obj, 508, CO_OPTIMIZED | CO_NEWLOCALS | CO_VARARGS | CO_VARKEYWORDS | CO_NOFREE, mod_consts[82], mod_consts[82], mod_consts[120], NULL, 4, 0, 0);
    codeobj_35e4dba3786838d11c6792c05107d109 = MAKE_CODE_OBJECT(module_filename_obj, 527, CO_OPTIMIZED | CO_NEWLOCALS | CO_VARARGS | CO_VARKEYWORDS | CO_NOFREE, mod_consts[84], mod_consts[84], mod_consts[121], NULL, 5, 0, 0);
    codeobj_489b9d905bb815d7f1578d1548e010e5 = MAKE_CODE_OBJECT(module_filename_obj, 543, CO_OPTIMIZED | CO_NEWLOCALS | CO_VARARGS | CO_VARKEYWORDS | CO_NOFREE, mod_consts[86], mod_consts[86], mod_consts[122], NULL, 5, 0, 0);
    codeobj_99168fe18391008f5fa4fc4155dd7815 = MAKE_CODE_OBJECT(module_filename_obj, 561, CO_OPTIMIZED | CO_NEWLOCALS | CO_VARARGS | CO_VARKEYWORDS | CO_NOFREE, mod_consts[88], mod_consts[88], mod_consts[123], NULL, 5, 0, 0);
}

// The module function declarations.
NUITKA_CROSS_MODULE PyObject *impl___main__$$$function__3_complex_call_helper_pos_star_list_star_dict(PyObject **python_pars);


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__10_invalidate_authorization_code();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__11_revoke_token();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__12_rotate_refresh_token();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__13_save_authorization_code();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__14_save_token();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__15_save_bearer_token();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__16_validate_bearer_token();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__17_validate_client_id();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__18_validate_code();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__19_validate_grant_type();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__1_client_authentication_required();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__20_validate_redirect_uri();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__21_validate_refresh_token();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__22_validate_response_type();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__23_validate_scopes();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__24_validate_user();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__25_is_pkce_required();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__26_get_code_challenge();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__27_get_code_challenge_method();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__28_is_origin_allowed();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__2_authenticate_client();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__3_authenticate_client_id();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__4_confirm_redirect_uri();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__5_get_default_redirect_uri();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__6_get_default_scopes();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__7_get_original_scopes();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__8_is_within_original_scope();


static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__9_introspect_token();


// The module function definitions.
static PyObject *impl_oauthlib$oauth2$rfc6749$request_validator$$$function__2_authenticate_client(struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_self = python_pars[0];
    PyObject *par_request = python_pars[1];
    PyObject *par_args = python_pars[2];
    PyObject *par_kwargs = python_pars[3];
    struct Nuitka_FrameObject *frame_cb20c4dfbed080a14a85811f41839e22;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    static struct Nuitka_FrameObject *cache_frame_cb20c4dfbed080a14a85811f41839e22 = NULL;

    // Actual function body.
    if (isFrameUnusable(cache_frame_cb20c4dfbed080a14a85811f41839e22)) {
        Py_XDECREF(cache_frame_cb20c4dfbed080a14a85811f41839e22);

#if _DEBUG_REFCOUNTS
        if (cache_frame_cb20c4dfbed080a14a85811f41839e22 == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_cb20c4dfbed080a14a85811f41839e22 = MAKE_FUNCTION_FRAME(codeobj_cb20c4dfbed080a14a85811f41839e22, module_oauthlib$oauth2$rfc6749$request_validator, sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_cb20c4dfbed080a14a85811f41839e22->m_type_description == NULL);
    frame_cb20c4dfbed080a14a85811f41839e22 = cache_frame_cb20c4dfbed080a14a85811f41839e22;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(frame_cb20c4dfbed080a14a85811f41839e22);
    assert(Py_REFCNT(frame_cb20c4dfbed080a14a85811f41839e22) == 2);

    // Framed code:
    {
        PyObject *tmp_raise_type_1;
        PyObject *tmp_make_exception_arg_1;
        tmp_make_exception_arg_1 = mod_consts[0];
        frame_cb20c4dfbed080a14a85811f41839e22->m_frame.f_lineno = 75;
        tmp_raise_type_1 = CALL_FUNCTION_WITH_SINGLE_ARG(PyExc_NotImplementedError, tmp_make_exception_arg_1);
        assert(!(tmp_raise_type_1 == NULL));
        exception_type = tmp_raise_type_1;
        exception_lineno = 75;
        RAISE_EXCEPTION_WITH_TYPE(&exception_type, &exception_value, &exception_tb);
        type_description_1 = "oooo";
        goto frame_exception_exit_1;
    }


    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;
    frame_exception_exit_1:


    if (exception_tb == NULL) {
        exception_tb = MAKE_TRACEBACK(frame_cb20c4dfbed080a14a85811f41839e22, exception_lineno);
    } else if (exception_tb->tb_frame != &frame_cb20c4dfbed080a14a85811f41839e22->m_frame) {
        exception_tb = ADD_TRACEBACK(exception_tb, frame_cb20c4dfbed080a14a85811f41839e22, exception_lineno);
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_cb20c4dfbed080a14a85811f41839e22,
        type_description_1,
        par_self,
        par_request,
        par_args,
        par_kwargs
    );


    // Release cached frame if used for exception.
    if (frame_cb20c4dfbed080a14a85811f41839e22 == cache_frame_cb20c4dfbed080a14a85811f41839e22) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_cb20c4dfbed080a14a85811f41839e22);
        cache_frame_cb20c4dfbed080a14a85811f41839e22 = NULL;
    }

    assertFrameObject(frame_cb20c4dfbed080a14a85811f41839e22);

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto function_exception_exit;
    frame_no_exception_1:;

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_request);
    Py_DECREF(par_request);
    CHECK_OBJECT(par_args);
    Py_DECREF(par_args);
    CHECK_OBJECT(par_kwargs);
    Py_DECREF(par_kwargs);
    assert(exception_type);
    RESTORE_ERROR_OCCURRED(exception_type, exception_value, exception_tb);

    return NULL;

}


static PyObject *impl_oauthlib$oauth2$rfc6749$request_validator$$$function__3_authenticate_client_id(struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_self = python_pars[0];
    PyObject *par_client_id = python_pars[1];
    PyObject *par_request = python_pars[2];
    PyObject *par_args = python_pars[3];
    PyObject *par_kwargs = python_pars[4];
    struct Nuitka_FrameObject *frame_176cec46e6b5ee76aee1ea4e54060d30;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    static struct Nuitka_FrameObject *cache_frame_176cec46e6b5ee76aee1ea4e54060d30 = NULL;

    // Actual function body.
    if (isFrameUnusable(cache_frame_176cec46e6b5ee76aee1ea4e54060d30)) {
        Py_XDECREF(cache_frame_176cec46e6b5ee76aee1ea4e54060d30);

#if _DEBUG_REFCOUNTS
        if (cache_frame_176cec46e6b5ee76aee1ea4e54060d30 == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_176cec46e6b5ee76aee1ea4e54060d30 = MAKE_FUNCTION_FRAME(codeobj_176cec46e6b5ee76aee1ea4e54060d30, module_oauthlib$oauth2$rfc6749$request_validator, sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_176cec46e6b5ee76aee1ea4e54060d30->m_type_description == NULL);
    frame_176cec46e6b5ee76aee1ea4e54060d30 = cache_frame_176cec46e6b5ee76aee1ea4e54060d30;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(frame_176cec46e6b5ee76aee1ea4e54060d30);
    assert(Py_REFCNT(frame_176cec46e6b5ee76aee1ea4e54060d30) == 2);

    // Framed code:
    {
        PyObject *tmp_raise_type_1;
        PyObject *tmp_make_exception_arg_1;
        tmp_make_exception_arg_1 = mod_consts[0];
        frame_176cec46e6b5ee76aee1ea4e54060d30->m_frame.f_lineno = 95;
        tmp_raise_type_1 = CALL_FUNCTION_WITH_SINGLE_ARG(PyExc_NotImplementedError, tmp_make_exception_arg_1);
        assert(!(tmp_raise_type_1 == NULL));
        exception_type = tmp_raise_type_1;
        exception_lineno = 95;
        RAISE_EXCEPTION_WITH_TYPE(&exception_type, &exception_value, &exception_tb);
        type_description_1 = "ooooo";
        goto frame_exception_exit_1;
    }


    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;
    frame_exception_exit_1:


    if (exception_tb == NULL) {
        exception_tb = MAKE_TRACEBACK(frame_176cec46e6b5ee76aee1ea4e54060d30, exception_lineno);
    } else if (exception_tb->tb_frame != &frame_176cec46e6b5ee76aee1ea4e54060d30->m_frame) {
        exception_tb = ADD_TRACEBACK(exception_tb, frame_176cec46e6b5ee76aee1ea4e54060d30, exception_lineno);
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_176cec46e6b5ee76aee1ea4e54060d30,
        type_description_1,
        par_self,
        par_client_id,
        par_request,
        par_args,
        par_kwargs
    );


    // Release cached frame if used for exception.
    if (frame_176cec46e6b5ee76aee1ea4e54060d30 == cache_frame_176cec46e6b5ee76aee1ea4e54060d30) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_176cec46e6b5ee76aee1ea4e54060d30);
        cache_frame_176cec46e6b5ee76aee1ea4e54060d30 = NULL;
    }

    assertFrameObject(frame_176cec46e6b5ee76aee1ea4e54060d30);

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto function_exception_exit;
    frame_no_exception_1:;

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_client_id);
    Py_DECREF(par_client_id);
    CHECK_OBJECT(par_request);
    Py_DECREF(par_request);
    CHECK_OBJECT(par_args);
    Py_DECREF(par_args);
    CHECK_OBJECT(par_kwargs);
    Py_DECREF(par_kwargs);
    assert(exception_type);
    RESTORE_ERROR_OCCURRED(exception_type, exception_value, exception_tb);

    return NULL;

}


static PyObject *impl_oauthlib$oauth2$rfc6749$request_validator$$$function__4_confirm_redirect_uri(struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_self = python_pars[0];
    PyObject *par_client_id = python_pars[1];
    PyObject *par_code = python_pars[2];
    PyObject *par_redirect_uri = python_pars[3];
    PyObject *par_client = python_pars[4];
    PyObject *par_request = python_pars[5];
    PyObject *par_args = python_pars[6];
    PyObject *par_kwargs = python_pars[7];
    struct Nuitka_FrameObject *frame_2a16f0793529ed9c7bae140e1ea16ad2;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    static struct Nuitka_FrameObject *cache_frame_2a16f0793529ed9c7bae140e1ea16ad2 = NULL;

    // Actual function body.
    if (isFrameUnusable(cache_frame_2a16f0793529ed9c7bae140e1ea16ad2)) {
        Py_XDECREF(cache_frame_2a16f0793529ed9c7bae140e1ea16ad2);

#if _DEBUG_REFCOUNTS
        if (cache_frame_2a16f0793529ed9c7bae140e1ea16ad2 == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_2a16f0793529ed9c7bae140e1ea16ad2 = MAKE_FUNCTION_FRAME(codeobj_2a16f0793529ed9c7bae140e1ea16ad2, module_oauthlib$oauth2$rfc6749$request_validator, sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_2a16f0793529ed9c7bae140e1ea16ad2->m_type_description == NULL);
    frame_2a16f0793529ed9c7bae140e1ea16ad2 = cache_frame_2a16f0793529ed9c7bae140e1ea16ad2;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(frame_2a16f0793529ed9c7bae140e1ea16ad2);
    assert(Py_REFCNT(frame_2a16f0793529ed9c7bae140e1ea16ad2) == 2);

    // Framed code:
    {
        PyObject *tmp_raise_type_1;
        PyObject *tmp_make_exception_arg_1;
        tmp_make_exception_arg_1 = mod_consts[0];
        frame_2a16f0793529ed9c7bae140e1ea16ad2->m_frame.f_lineno = 119;
        tmp_raise_type_1 = CALL_FUNCTION_WITH_SINGLE_ARG(PyExc_NotImplementedError, tmp_make_exception_arg_1);
        assert(!(tmp_raise_type_1 == NULL));
        exception_type = tmp_raise_type_1;
        exception_lineno = 119;
        RAISE_EXCEPTION_WITH_TYPE(&exception_type, &exception_value, &exception_tb);
        type_description_1 = "oooooooo";
        goto frame_exception_exit_1;
    }


    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;
    frame_exception_exit_1:


    if (exception_tb == NULL) {
        exception_tb = MAKE_TRACEBACK(frame_2a16f0793529ed9c7bae140e1ea16ad2, exception_lineno);
    } else if (exception_tb->tb_frame != &frame_2a16f0793529ed9c7bae140e1ea16ad2->m_frame) {
        exception_tb = ADD_TRACEBACK(exception_tb, frame_2a16f0793529ed9c7bae140e1ea16ad2, exception_lineno);
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_2a16f0793529ed9c7bae140e1ea16ad2,
        type_description_1,
        par_self,
        par_client_id,
        par_code,
        par_redirect_uri,
        par_client,
        par_request,
        par_args,
        par_kwargs
    );


    // Release cached frame if used for exception.
    if (frame_2a16f0793529ed9c7bae140e1ea16ad2 == cache_frame_2a16f0793529ed9c7bae140e1ea16ad2) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_2a16f0793529ed9c7bae140e1ea16ad2);
        cache_frame_2a16f0793529ed9c7bae140e1ea16ad2 = NULL;
    }

    assertFrameObject(frame_2a16f0793529ed9c7bae140e1ea16ad2);

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto function_exception_exit;
    frame_no_exception_1:;

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_client_id);
    Py_DECREF(par_client_id);
    CHECK_OBJECT(par_code);
    Py_DECREF(par_code);
    CHECK_OBJECT(par_redirect_uri);
    Py_DECREF(par_redirect_uri);
    CHECK_OBJECT(par_client);
    Py_DECREF(par_client);
    CHECK_OBJECT(par_request);
    Py_DECREF(par_request);
    CHECK_OBJECT(par_args);
    Py_DECREF(par_args);
    CHECK_OBJECT(par_kwargs);
    Py_DECREF(par_kwargs);
    assert(exception_type);
    RESTORE_ERROR_OCCURRED(exception_type, exception_value, exception_tb);

    return NULL;

}


static PyObject *impl_oauthlib$oauth2$rfc6749$request_validator$$$function__5_get_default_redirect_uri(struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_self = python_pars[0];
    PyObject *par_client_id = python_pars[1];
    PyObject *par_request = python_pars[2];
    PyObject *par_args = python_pars[3];
    PyObject *par_kwargs = python_pars[4];
    struct Nuitka_FrameObject *frame_dfb0755ba293c104853cc61335c50977;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    static struct Nuitka_FrameObject *cache_frame_dfb0755ba293c104853cc61335c50977 = NULL;

    // Actual function body.
    if (isFrameUnusable(cache_frame_dfb0755ba293c104853cc61335c50977)) {
        Py_XDECREF(cache_frame_dfb0755ba293c104853cc61335c50977);

#if _DEBUG_REFCOUNTS
        if (cache_frame_dfb0755ba293c104853cc61335c50977 == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_dfb0755ba293c104853cc61335c50977 = MAKE_FUNCTION_FRAME(codeobj_dfb0755ba293c104853cc61335c50977, module_oauthlib$oauth2$rfc6749$request_validator, sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_dfb0755ba293c104853cc61335c50977->m_type_description == NULL);
    frame_dfb0755ba293c104853cc61335c50977 = cache_frame_dfb0755ba293c104853cc61335c50977;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(frame_dfb0755ba293c104853cc61335c50977);
    assert(Py_REFCNT(frame_dfb0755ba293c104853cc61335c50977) == 2);

    // Framed code:
    {
        PyObject *tmp_raise_type_1;
        PyObject *tmp_make_exception_arg_1;
        tmp_make_exception_arg_1 = mod_consts[0];
        frame_dfb0755ba293c104853cc61335c50977->m_frame.f_lineno = 133;
        tmp_raise_type_1 = CALL_FUNCTION_WITH_SINGLE_ARG(PyExc_NotImplementedError, tmp_make_exception_arg_1);
        assert(!(tmp_raise_type_1 == NULL));
        exception_type = tmp_raise_type_1;
        exception_lineno = 133;
        RAISE_EXCEPTION_WITH_TYPE(&exception_type, &exception_value, &exception_tb);
        type_description_1 = "ooooo";
        goto frame_exception_exit_1;
    }


    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;
    frame_exception_exit_1:


    if (exception_tb == NULL) {
        exception_tb = MAKE_TRACEBACK(frame_dfb0755ba293c104853cc61335c50977, exception_lineno);
    } else if (exception_tb->tb_frame != &frame_dfb0755ba293c104853cc61335c50977->m_frame) {
        exception_tb = ADD_TRACEBACK(exception_tb, frame_dfb0755ba293c104853cc61335c50977, exception_lineno);
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_dfb0755ba293c104853cc61335c50977,
        type_description_1,
        par_self,
        par_client_id,
        par_request,
        par_args,
        par_kwargs
    );


    // Release cached frame if used for exception.
    if (frame_dfb0755ba293c104853cc61335c50977 == cache_frame_dfb0755ba293c104853cc61335c50977) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_dfb0755ba293c104853cc61335c50977);
        cache_frame_dfb0755ba293c104853cc61335c50977 = NULL;
    }

    assertFrameObject(frame_dfb0755ba293c104853cc61335c50977);

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto function_exception_exit;
    frame_no_exception_1:;

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_client_id);
    Py_DECREF(par_client_id);
    CHECK_OBJECT(par_request);
    Py_DECREF(par_request);
    CHECK_OBJECT(par_args);
    Py_DECREF(par_args);
    CHECK_OBJECT(par_kwargs);
    Py_DECREF(par_kwargs);
    assert(exception_type);
    RESTORE_ERROR_OCCURRED(exception_type, exception_value, exception_tb);

    return NULL;

}


static PyObject *impl_oauthlib$oauth2$rfc6749$request_validator$$$function__6_get_default_scopes(struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_self = python_pars[0];
    PyObject *par_client_id = python_pars[1];
    PyObject *par_request = python_pars[2];
    PyObject *par_args = python_pars[3];
    PyObject *par_kwargs = python_pars[4];
    struct Nuitka_FrameObject *frame_41a3ece1a35709f73a6c917b7c80bf46;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    static struct Nuitka_FrameObject *cache_frame_41a3ece1a35709f73a6c917b7c80bf46 = NULL;

    // Actual function body.
    if (isFrameUnusable(cache_frame_41a3ece1a35709f73a6c917b7c80bf46)) {
        Py_XDECREF(cache_frame_41a3ece1a35709f73a6c917b7c80bf46);

#if _DEBUG_REFCOUNTS
        if (cache_frame_41a3ece1a35709f73a6c917b7c80bf46 == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_41a3ece1a35709f73a6c917b7c80bf46 = MAKE_FUNCTION_FRAME(codeobj_41a3ece1a35709f73a6c917b7c80bf46, module_oauthlib$oauth2$rfc6749$request_validator, sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_41a3ece1a35709f73a6c917b7c80bf46->m_type_description == NULL);
    frame_41a3ece1a35709f73a6c917b7c80bf46 = cache_frame_41a3ece1a35709f73a6c917b7c80bf46;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(frame_41a3ece1a35709f73a6c917b7c80bf46);
    assert(Py_REFCNT(frame_41a3ece1a35709f73a6c917b7c80bf46) == 2);

    // Framed code:
    {
        PyObject *tmp_raise_type_1;
        PyObject *tmp_make_exception_arg_1;
        tmp_make_exception_arg_1 = mod_consts[0];
        frame_41a3ece1a35709f73a6c917b7c80bf46->m_frame.f_lineno = 149;
        tmp_raise_type_1 = CALL_FUNCTION_WITH_SINGLE_ARG(PyExc_NotImplementedError, tmp_make_exception_arg_1);
        assert(!(tmp_raise_type_1 == NULL));
        exception_type = tmp_raise_type_1;
        exception_lineno = 149;
        RAISE_EXCEPTION_WITH_TYPE(&exception_type, &exception_value, &exception_tb);
        type_description_1 = "ooooo";
        goto frame_exception_exit_1;
    }


    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;
    frame_exception_exit_1:


    if (exception_tb == NULL) {
        exception_tb = MAKE_TRACEBACK(frame_41a3ece1a35709f73a6c917b7c80bf46, exception_lineno);
    } else if (exception_tb->tb_frame != &frame_41a3ece1a35709f73a6c917b7c80bf46->m_frame) {
        exception_tb = ADD_TRACEBACK(exception_tb, frame_41a3ece1a35709f73a6c917b7c80bf46, exception_lineno);
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_41a3ece1a35709f73a6c917b7c80bf46,
        type_description_1,
        par_self,
        par_client_id,
        par_request,
        par_args,
        par_kwargs
    );


    // Release cached frame if used for exception.
    if (frame_41a3ece1a35709f73a6c917b7c80bf46 == cache_frame_41a3ece1a35709f73a6c917b7c80bf46) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_41a3ece1a35709f73a6c917b7c80bf46);
        cache_frame_41a3ece1a35709f73a6c917b7c80bf46 = NULL;
    }

    assertFrameObject(frame_41a3ece1a35709f73a6c917b7c80bf46);

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto function_exception_exit;
    frame_no_exception_1:;

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_client_id);
    Py_DECREF(par_client_id);
    CHECK_OBJECT(par_request);
    Py_DECREF(par_request);
    CHECK_OBJECT(par_args);
    Py_DECREF(par_args);
    CHECK_OBJECT(par_kwargs);
    Py_DECREF(par_kwargs);
    assert(exception_type);
    RESTORE_ERROR_OCCURRED(exception_type, exception_value, exception_tb);

    return NULL;

}


static PyObject *impl_oauthlib$oauth2$rfc6749$request_validator$$$function__7_get_original_scopes(struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_self = python_pars[0];
    PyObject *par_refresh_token = python_pars[1];
    PyObject *par_request = python_pars[2];
    PyObject *par_args = python_pars[3];
    PyObject *par_kwargs = python_pars[4];
    struct Nuitka_FrameObject *frame_17f5e2b7f4eac3a3190f4cbbed334286;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    static struct Nuitka_FrameObject *cache_frame_17f5e2b7f4eac3a3190f4cbbed334286 = NULL;

    // Actual function body.
    if (isFrameUnusable(cache_frame_17f5e2b7f4eac3a3190f4cbbed334286)) {
        Py_XDECREF(cache_frame_17f5e2b7f4eac3a3190f4cbbed334286);

#if _DEBUG_REFCOUNTS
        if (cache_frame_17f5e2b7f4eac3a3190f4cbbed334286 == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_17f5e2b7f4eac3a3190f4cbbed334286 = MAKE_FUNCTION_FRAME(codeobj_17f5e2b7f4eac3a3190f4cbbed334286, module_oauthlib$oauth2$rfc6749$request_validator, sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_17f5e2b7f4eac3a3190f4cbbed334286->m_type_description == NULL);
    frame_17f5e2b7f4eac3a3190f4cbbed334286 = cache_frame_17f5e2b7f4eac3a3190f4cbbed334286;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(frame_17f5e2b7f4eac3a3190f4cbbed334286);
    assert(Py_REFCNT(frame_17f5e2b7f4eac3a3190f4cbbed334286) == 2);

    // Framed code:
    {
        PyObject *tmp_raise_type_1;
        PyObject *tmp_make_exception_arg_1;
        tmp_make_exception_arg_1 = mod_consts[0];
        frame_17f5e2b7f4eac3a3190f4cbbed334286->m_frame.f_lineno = 162;
        tmp_raise_type_1 = CALL_FUNCTION_WITH_SINGLE_ARG(PyExc_NotImplementedError, tmp_make_exception_arg_1);
        assert(!(tmp_raise_type_1 == NULL));
        exception_type = tmp_raise_type_1;
        exception_lineno = 162;
        RAISE_EXCEPTION_WITH_TYPE(&exception_type, &exception_value, &exception_tb);
        type_description_1 = "ooooo";
        goto frame_exception_exit_1;
    }


    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;
    frame_exception_exit_1:


    if (exception_tb == NULL) {
        exception_tb = MAKE_TRACEBACK(frame_17f5e2b7f4eac3a3190f4cbbed334286, exception_lineno);
    } else if (exception_tb->tb_frame != &frame_17f5e2b7f4eac3a3190f4cbbed334286->m_frame) {
        exception_tb = ADD_TRACEBACK(exception_tb, frame_17f5e2b7f4eac3a3190f4cbbed334286, exception_lineno);
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_17f5e2b7f4eac3a3190f4cbbed334286,
        type_description_1,
        par_self,
        par_refresh_token,
        par_request,
        par_args,
        par_kwargs
    );


    // Release cached frame if used for exception.
    if (frame_17f5e2b7f4eac3a3190f4cbbed334286 == cache_frame_17f5e2b7f4eac3a3190f4cbbed334286) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_17f5e2b7f4eac3a3190f4cbbed334286);
        cache_frame_17f5e2b7f4eac3a3190f4cbbed334286 = NULL;
    }

    assertFrameObject(frame_17f5e2b7f4eac3a3190f4cbbed334286);

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto function_exception_exit;
    frame_no_exception_1:;

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_refresh_token);
    Py_DECREF(par_refresh_token);
    CHECK_OBJECT(par_request);
    Py_DECREF(par_request);
    CHECK_OBJECT(par_args);
    Py_DECREF(par_args);
    CHECK_OBJECT(par_kwargs);
    Py_DECREF(par_kwargs);
    assert(exception_type);
    RESTORE_ERROR_OCCURRED(exception_type, exception_value, exception_tb);

    return NULL;

}


static PyObject *impl_oauthlib$oauth2$rfc6749$request_validator$$$function__9_introspect_token(struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_self = python_pars[0];
    PyObject *par_token = python_pars[1];
    PyObject *par_token_type_hint = python_pars[2];
    PyObject *par_request = python_pars[3];
    PyObject *par_args = python_pars[4];
    PyObject *par_kwargs = python_pars[5];
    struct Nuitka_FrameObject *frame_f2c4f529262545335009559750e8e70e;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    static struct Nuitka_FrameObject *cache_frame_f2c4f529262545335009559750e8e70e = NULL;

    // Actual function body.
    if (isFrameUnusable(cache_frame_f2c4f529262545335009559750e8e70e)) {
        Py_XDECREF(cache_frame_f2c4f529262545335009559750e8e70e);

#if _DEBUG_REFCOUNTS
        if (cache_frame_f2c4f529262545335009559750e8e70e == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_f2c4f529262545335009559750e8e70e = MAKE_FUNCTION_FRAME(codeobj_f2c4f529262545335009559750e8e70e, module_oauthlib$oauth2$rfc6749$request_validator, sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_f2c4f529262545335009559750e8e70e->m_type_description == NULL);
    frame_f2c4f529262545335009559750e8e70e = cache_frame_f2c4f529262545335009559750e8e70e;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(frame_f2c4f529262545335009559750e8e70e);
    assert(Py_REFCNT(frame_f2c4f529262545335009559750e8e70e) == 2);

    // Framed code:
    {
        PyObject *tmp_raise_type_1;
        PyObject *tmp_make_exception_arg_1;
        tmp_make_exception_arg_1 = mod_consts[0];
        frame_f2c4f529262545335009559750e8e70e->m_frame.f_lineno = 226;
        tmp_raise_type_1 = CALL_FUNCTION_WITH_SINGLE_ARG(PyExc_NotImplementedError, tmp_make_exception_arg_1);
        assert(!(tmp_raise_type_1 == NULL));
        exception_type = tmp_raise_type_1;
        exception_lineno = 226;
        RAISE_EXCEPTION_WITH_TYPE(&exception_type, &exception_value, &exception_tb);
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }


    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;
    frame_exception_exit_1:


    if (exception_tb == NULL) {
        exception_tb = MAKE_TRACEBACK(frame_f2c4f529262545335009559750e8e70e, exception_lineno);
    } else if (exception_tb->tb_frame != &frame_f2c4f529262545335009559750e8e70e->m_frame) {
        exception_tb = ADD_TRACEBACK(exception_tb, frame_f2c4f529262545335009559750e8e70e, exception_lineno);
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_f2c4f529262545335009559750e8e70e,
        type_description_1,
        par_self,
        par_token,
        par_token_type_hint,
        par_request,
        par_args,
        par_kwargs
    );


    // Release cached frame if used for exception.
    if (frame_f2c4f529262545335009559750e8e70e == cache_frame_f2c4f529262545335009559750e8e70e) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_f2c4f529262545335009559750e8e70e);
        cache_frame_f2c4f529262545335009559750e8e70e = NULL;
    }

    assertFrameObject(frame_f2c4f529262545335009559750e8e70e);

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto function_exception_exit;
    frame_no_exception_1:;

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_token);
    Py_DECREF(par_token);
    CHECK_OBJECT(par_token_type_hint);
    Py_DECREF(par_token_type_hint);
    CHECK_OBJECT(par_request);
    Py_DECREF(par_request);
    CHECK_OBJECT(par_args);
    Py_DECREF(par_args);
    CHECK_OBJECT(par_kwargs);
    Py_DECREF(par_kwargs);
    assert(exception_type);
    RESTORE_ERROR_OCCURRED(exception_type, exception_value, exception_tb);

    return NULL;

}


static PyObject *impl_oauthlib$oauth2$rfc6749$request_validator$$$function__10_invalidate_authorization_code(struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_self = python_pars[0];
    PyObject *par_client_id = python_pars[1];
    PyObject *par_code = python_pars[2];
    PyObject *par_request = python_pars[3];
    PyObject *par_args = python_pars[4];
    PyObject *par_kwargs = python_pars[5];
    struct Nuitka_FrameObject *frame_eb455e7e8b0726ab205bddb0b5032af7;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    static struct Nuitka_FrameObject *cache_frame_eb455e7e8b0726ab205bddb0b5032af7 = NULL;

    // Actual function body.
    if (isFrameUnusable(cache_frame_eb455e7e8b0726ab205bddb0b5032af7)) {
        Py_XDECREF(cache_frame_eb455e7e8b0726ab205bddb0b5032af7);

#if _DEBUG_REFCOUNTS
        if (cache_frame_eb455e7e8b0726ab205bddb0b5032af7 == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_eb455e7e8b0726ab205bddb0b5032af7 = MAKE_FUNCTION_FRAME(codeobj_eb455e7e8b0726ab205bddb0b5032af7, module_oauthlib$oauth2$rfc6749$request_validator, sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_eb455e7e8b0726ab205bddb0b5032af7->m_type_description == NULL);
    frame_eb455e7e8b0726ab205bddb0b5032af7 = cache_frame_eb455e7e8b0726ab205bddb0b5032af7;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(frame_eb455e7e8b0726ab205bddb0b5032af7);
    assert(Py_REFCNT(frame_eb455e7e8b0726ab205bddb0b5032af7) == 2);

    // Framed code:
    {
        PyObject *tmp_raise_type_1;
        PyObject *tmp_make_exception_arg_1;
        tmp_make_exception_arg_1 = mod_consts[0];
        frame_eb455e7e8b0726ab205bddb0b5032af7->m_frame.f_lineno = 239;
        tmp_raise_type_1 = CALL_FUNCTION_WITH_SINGLE_ARG(PyExc_NotImplementedError, tmp_make_exception_arg_1);
        assert(!(tmp_raise_type_1 == NULL));
        exception_type = tmp_raise_type_1;
        exception_lineno = 239;
        RAISE_EXCEPTION_WITH_TYPE(&exception_type, &exception_value, &exception_tb);
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }


    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;
    frame_exception_exit_1:


    if (exception_tb == NULL) {
        exception_tb = MAKE_TRACEBACK(frame_eb455e7e8b0726ab205bddb0b5032af7, exception_lineno);
    } else if (exception_tb->tb_frame != &frame_eb455e7e8b0726ab205bddb0b5032af7->m_frame) {
        exception_tb = ADD_TRACEBACK(exception_tb, frame_eb455e7e8b0726ab205bddb0b5032af7, exception_lineno);
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_eb455e7e8b0726ab205bddb0b5032af7,
        type_description_1,
        par_self,
        par_client_id,
        par_code,
        par_request,
        par_args,
        par_kwargs
    );


    // Release cached frame if used for exception.
    if (frame_eb455e7e8b0726ab205bddb0b5032af7 == cache_frame_eb455e7e8b0726ab205bddb0b5032af7) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_eb455e7e8b0726ab205bddb0b5032af7);
        cache_frame_eb455e7e8b0726ab205bddb0b5032af7 = NULL;
    }

    assertFrameObject(frame_eb455e7e8b0726ab205bddb0b5032af7);

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto function_exception_exit;
    frame_no_exception_1:;

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_client_id);
    Py_DECREF(par_client_id);
    CHECK_OBJECT(par_code);
    Py_DECREF(par_code);
    CHECK_OBJECT(par_request);
    Py_DECREF(par_request);
    CHECK_OBJECT(par_args);
    Py_DECREF(par_args);
    CHECK_OBJECT(par_kwargs);
    Py_DECREF(par_kwargs);
    assert(exception_type);
    RESTORE_ERROR_OCCURRED(exception_type, exception_value, exception_tb);

    return NULL;

}


static PyObject *impl_oauthlib$oauth2$rfc6749$request_validator$$$function__11_revoke_token(struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_self = python_pars[0];
    PyObject *par_token = python_pars[1];
    PyObject *par_token_type_hint = python_pars[2];
    PyObject *par_request = python_pars[3];
    PyObject *par_args = python_pars[4];
    PyObject *par_kwargs = python_pars[5];
    struct Nuitka_FrameObject *frame_88f698014760404e5103d09728eed55f;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    static struct Nuitka_FrameObject *cache_frame_88f698014760404e5103d09728eed55f = NULL;

    // Actual function body.
    if (isFrameUnusable(cache_frame_88f698014760404e5103d09728eed55f)) {
        Py_XDECREF(cache_frame_88f698014760404e5103d09728eed55f);

#if _DEBUG_REFCOUNTS
        if (cache_frame_88f698014760404e5103d09728eed55f == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_88f698014760404e5103d09728eed55f = MAKE_FUNCTION_FRAME(codeobj_88f698014760404e5103d09728eed55f, module_oauthlib$oauth2$rfc6749$request_validator, sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_88f698014760404e5103d09728eed55f->m_type_description == NULL);
    frame_88f698014760404e5103d09728eed55f = cache_frame_88f698014760404e5103d09728eed55f;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(frame_88f698014760404e5103d09728eed55f);
    assert(Py_REFCNT(frame_88f698014760404e5103d09728eed55f) == 2);

    // Framed code:
    {
        PyObject *tmp_raise_type_1;
        PyObject *tmp_make_exception_arg_1;
        tmp_make_exception_arg_1 = mod_consts[0];
        frame_88f698014760404e5103d09728eed55f->m_frame.f_lineno = 252;
        tmp_raise_type_1 = CALL_FUNCTION_WITH_SINGLE_ARG(PyExc_NotImplementedError, tmp_make_exception_arg_1);
        assert(!(tmp_raise_type_1 == NULL));
        exception_type = tmp_raise_type_1;
        exception_lineno = 252;
        RAISE_EXCEPTION_WITH_TYPE(&exception_type, &exception_value, &exception_tb);
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }


    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;
    frame_exception_exit_1:


    if (exception_tb == NULL) {
        exception_tb = MAKE_TRACEBACK(frame_88f698014760404e5103d09728eed55f, exception_lineno);
    } else if (exception_tb->tb_frame != &frame_88f698014760404e5103d09728eed55f->m_frame) {
        exception_tb = ADD_TRACEBACK(exception_tb, frame_88f698014760404e5103d09728eed55f, exception_lineno);
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_88f698014760404e5103d09728eed55f,
        type_description_1,
        par_self,
        par_token,
        par_token_type_hint,
        par_request,
        par_args,
        par_kwargs
    );


    // Release cached frame if used for exception.
    if (frame_88f698014760404e5103d09728eed55f == cache_frame_88f698014760404e5103d09728eed55f) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_88f698014760404e5103d09728eed55f);
        cache_frame_88f698014760404e5103d09728eed55f = NULL;
    }

    assertFrameObject(frame_88f698014760404e5103d09728eed55f);

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto function_exception_exit;
    frame_no_exception_1:;

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_token);
    Py_DECREF(par_token);
    CHECK_OBJECT(par_token_type_hint);
    Py_DECREF(par_token_type_hint);
    CHECK_OBJECT(par_request);
    Py_DECREF(par_request);
    CHECK_OBJECT(par_args);
    Py_DECREF(par_args);
    CHECK_OBJECT(par_kwargs);
    Py_DECREF(par_kwargs);
    assert(exception_type);
    RESTORE_ERROR_OCCURRED(exception_type, exception_value, exception_tb);

    return NULL;

}


static PyObject *impl_oauthlib$oauth2$rfc6749$request_validator$$$function__13_save_authorization_code(struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_self = python_pars[0];
    PyObject *par_client_id = python_pars[1];
    PyObject *par_code = python_pars[2];
    PyObject *par_request = python_pars[3];
    PyObject *par_args = python_pars[4];
    PyObject *par_kwargs = python_pars[5];
    struct Nuitka_FrameObject *frame_a60172c1215f2f00cf0915196d66e963;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    static struct Nuitka_FrameObject *cache_frame_a60172c1215f2f00cf0915196d66e963 = NULL;

    // Actual function body.
    if (isFrameUnusable(cache_frame_a60172c1215f2f00cf0915196d66e963)) {
        Py_XDECREF(cache_frame_a60172c1215f2f00cf0915196d66e963);

#if _DEBUG_REFCOUNTS
        if (cache_frame_a60172c1215f2f00cf0915196d66e963 == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_a60172c1215f2f00cf0915196d66e963 = MAKE_FUNCTION_FRAME(codeobj_a60172c1215f2f00cf0915196d66e963, module_oauthlib$oauth2$rfc6749$request_validator, sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_a60172c1215f2f00cf0915196d66e963->m_type_description == NULL);
    frame_a60172c1215f2f00cf0915196d66e963 = cache_frame_a60172c1215f2f00cf0915196d66e963;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(frame_a60172c1215f2f00cf0915196d66e963);
    assert(Py_REFCNT(frame_a60172c1215f2f00cf0915196d66e963) == 2);

    // Framed code:
    {
        PyObject *tmp_raise_type_1;
        PyObject *tmp_make_exception_arg_1;
        tmp_make_exception_arg_1 = mod_consts[0];
        frame_a60172c1215f2f00cf0915196d66e963->m_frame.f_lineno = 304;
        tmp_raise_type_1 = CALL_FUNCTION_WITH_SINGLE_ARG(PyExc_NotImplementedError, tmp_make_exception_arg_1);
        assert(!(tmp_raise_type_1 == NULL));
        exception_type = tmp_raise_type_1;
        exception_lineno = 304;
        RAISE_EXCEPTION_WITH_TYPE(&exception_type, &exception_value, &exception_tb);
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }


    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;
    frame_exception_exit_1:


    if (exception_tb == NULL) {
        exception_tb = MAKE_TRACEBACK(frame_a60172c1215f2f00cf0915196d66e963, exception_lineno);
    } else if (exception_tb->tb_frame != &frame_a60172c1215f2f00cf0915196d66e963->m_frame) {
        exception_tb = ADD_TRACEBACK(exception_tb, frame_a60172c1215f2f00cf0915196d66e963, exception_lineno);
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_a60172c1215f2f00cf0915196d66e963,
        type_description_1,
        par_self,
        par_client_id,
        par_code,
        par_request,
        par_args,
        par_kwargs
    );


    // Release cached frame if used for exception.
    if (frame_a60172c1215f2f00cf0915196d66e963 == cache_frame_a60172c1215f2f00cf0915196d66e963) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_a60172c1215f2f00cf0915196d66e963);
        cache_frame_a60172c1215f2f00cf0915196d66e963 = NULL;
    }

    assertFrameObject(frame_a60172c1215f2f00cf0915196d66e963);

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto function_exception_exit;
    frame_no_exception_1:;

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_client_id);
    Py_DECREF(par_client_id);
    CHECK_OBJECT(par_code);
    Py_DECREF(par_code);
    CHECK_OBJECT(par_request);
    Py_DECREF(par_request);
    CHECK_OBJECT(par_args);
    Py_DECREF(par_args);
    CHECK_OBJECT(par_kwargs);
    Py_DECREF(par_kwargs);
    assert(exception_type);
    RESTORE_ERROR_OCCURRED(exception_type, exception_value, exception_tb);

    return NULL;

}


static PyObject *impl_oauthlib$oauth2$rfc6749$request_validator$$$function__14_save_token(struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_self = python_pars[0];
    PyObject *par_token = python_pars[1];
    PyObject *par_request = python_pars[2];
    PyObject *par_args = python_pars[3];
    PyObject *par_kwargs = python_pars[4];
    struct Nuitka_FrameObject *frame_f6577c7b7854260253ce470c8440f149;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    PyObject *tmp_return_value = NULL;
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    static struct Nuitka_FrameObject *cache_frame_f6577c7b7854260253ce470c8440f149 = NULL;

    // Actual function body.
    if (isFrameUnusable(cache_frame_f6577c7b7854260253ce470c8440f149)) {
        Py_XDECREF(cache_frame_f6577c7b7854260253ce470c8440f149);

#if _DEBUG_REFCOUNTS
        if (cache_frame_f6577c7b7854260253ce470c8440f149 == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_f6577c7b7854260253ce470c8440f149 = MAKE_FUNCTION_FRAME(codeobj_f6577c7b7854260253ce470c8440f149, module_oauthlib$oauth2$rfc6749$request_validator, sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_f6577c7b7854260253ce470c8440f149->m_type_description == NULL);
    frame_f6577c7b7854260253ce470c8440f149 = cache_frame_f6577c7b7854260253ce470c8440f149;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(frame_f6577c7b7854260253ce470c8440f149);
    assert(Py_REFCNT(frame_f6577c7b7854260253ce470c8440f149) == 2);

    // Framed code:
    {
        PyObject *tmp_dircall_arg1_1;
        PyObject *tmp_expression_value_1;
        PyObject *tmp_dircall_arg2_1;
        PyObject *tmp_tuple_element_1;
        PyObject *tmp_dircall_arg3_1;
        PyObject *tmp_dircall_arg4_1;
        CHECK_OBJECT(par_self);
        tmp_expression_value_1 = par_self;
        tmp_dircall_arg1_1 = LOOKUP_ATTRIBUTE(tmp_expression_value_1, mod_consts[11]);
        if (tmp_dircall_arg1_1 == NULL) {
            assert(ERROR_OCCURRED());

            FETCH_ERROR_OCCURRED(&exception_type, &exception_value, &exception_tb);


            exception_lineno = 315;
            type_description_1 = "ooooo";
            goto frame_exception_exit_1;
        }
        CHECK_OBJECT(par_token);
        tmp_tuple_element_1 = par_token;
        tmp_dircall_arg2_1 = MAKE_TUPLE_EMPTY(2);
        PyTuple_SET_ITEM0(tmp_dircall_arg2_1, 0, tmp_tuple_element_1);
        CHECK_OBJECT(par_request);
        tmp_tuple_element_1 = par_request;
        PyTuple_SET_ITEM0(tmp_dircall_arg2_1, 1, tmp_tuple_element_1);
        CHECK_OBJECT(par_args);
        tmp_dircall_arg3_1 = par_args;
        CHECK_OBJECT(par_kwargs);
        tmp_dircall_arg4_1 = par_kwargs;
        Py_INCREF(tmp_dircall_arg3_1);
        Py_INCREF(tmp_dircall_arg4_1);

        {
            PyObject *dir_call_args[] = {tmp_dircall_arg1_1, tmp_dircall_arg2_1, tmp_dircall_arg3_1, tmp_dircall_arg4_1};
            tmp_return_value = impl___main__$$$function__3_complex_call_helper_pos_star_list_star_dict(dir_call_args);
        }
        if (tmp_return_value == NULL) {
            assert(ERROR_OCCURRED());

            FETCH_ERROR_OCCURRED(&exception_type, &exception_value, &exception_tb);


            exception_lineno = 315;
            type_description_1 = "ooooo";
            goto frame_exception_exit_1;
        }
        goto frame_return_exit_1;
    }


    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;
    frame_return_exit_1:

    // Put the previous frame back on top.
    popFrameStack();

    goto function_return_exit;
    frame_exception_exit_1:


    if (exception_tb == NULL) {
        exception_tb = MAKE_TRACEBACK(frame_f6577c7b7854260253ce470c8440f149, exception_lineno);
    } else if (exception_tb->tb_frame != &frame_f6577c7b7854260253ce470c8440f149->m_frame) {
        exception_tb = ADD_TRACEBACK(exception_tb, frame_f6577c7b7854260253ce470c8440f149, exception_lineno);
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_f6577c7b7854260253ce470c8440f149,
        type_description_1,
        par_self,
        par_token,
        par_request,
        par_args,
        par_kwargs
    );


    // Release cached frame if used for exception.
    if (frame_f6577c7b7854260253ce470c8440f149 == cache_frame_f6577c7b7854260253ce470c8440f149) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_f6577c7b7854260253ce470c8440f149);
        cache_frame_f6577c7b7854260253ce470c8440f149 = NULL;
    }

    assertFrameObject(frame_f6577c7b7854260253ce470c8440f149);

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto function_exception_exit;
    frame_no_exception_1:;

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_token);
    Py_DECREF(par_token);
    CHECK_OBJECT(par_request);
    Py_DECREF(par_request);
    CHECK_OBJECT(par_args);
    Py_DECREF(par_args);
    CHECK_OBJECT(par_kwargs);
    Py_DECREF(par_kwargs);
    assert(exception_type);
    RESTORE_ERROR_OCCURRED(exception_type, exception_value, exception_tb);

    return NULL;

function_return_exit:
   // Function cleanup code if any.
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_token);
    Py_DECREF(par_token);
    CHECK_OBJECT(par_request);
    Py_DECREF(par_request);
    CHECK_OBJECT(par_args);
    Py_DECREF(par_args);
    CHECK_OBJECT(par_kwargs);
    Py_DECREF(par_kwargs);

   // Actual function exit with return value, making sure we did not make
   // the error status worse despite non-NULL return.
   CHECK_OBJECT(tmp_return_value);
   assert(had_error || !ERROR_OCCURRED());
   return tmp_return_value;
}


static PyObject *impl_oauthlib$oauth2$rfc6749$request_validator$$$function__15_save_bearer_token(struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_self = python_pars[0];
    PyObject *par_token = python_pars[1];
    PyObject *par_request = python_pars[2];
    PyObject *par_args = python_pars[3];
    PyObject *par_kwargs = python_pars[4];
    struct Nuitka_FrameObject *frame_30c9aaa654910caf6b84f64746df29d8;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    static struct Nuitka_FrameObject *cache_frame_30c9aaa654910caf6b84f64746df29d8 = NULL;

    // Actual function body.
    if (isFrameUnusable(cache_frame_30c9aaa654910caf6b84f64746df29d8)) {
        Py_XDECREF(cache_frame_30c9aaa654910caf6b84f64746df29d8);

#if _DEBUG_REFCOUNTS
        if (cache_frame_30c9aaa654910caf6b84f64746df29d8 == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_30c9aaa654910caf6b84f64746df29d8 = MAKE_FUNCTION_FRAME(codeobj_30c9aaa654910caf6b84f64746df29d8, module_oauthlib$oauth2$rfc6749$request_validator, sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_30c9aaa654910caf6b84f64746df29d8->m_type_description == NULL);
    frame_30c9aaa654910caf6b84f64746df29d8 = cache_frame_30c9aaa654910caf6b84f64746df29d8;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(frame_30c9aaa654910caf6b84f64746df29d8);
    assert(Py_REFCNT(frame_30c9aaa654910caf6b84f64746df29d8) == 2);

    // Framed code:
    {
        PyObject *tmp_raise_type_1;
        PyObject *tmp_make_exception_arg_1;
        tmp_make_exception_arg_1 = mod_consts[0];
        frame_30c9aaa654910caf6b84f64746df29d8->m_frame.f_lineno = 365;
        tmp_raise_type_1 = CALL_FUNCTION_WITH_SINGLE_ARG(PyExc_NotImplementedError, tmp_make_exception_arg_1);
        assert(!(tmp_raise_type_1 == NULL));
        exception_type = tmp_raise_type_1;
        exception_lineno = 365;
        RAISE_EXCEPTION_WITH_TYPE(&exception_type, &exception_value, &exception_tb);
        type_description_1 = "ooooo";
        goto frame_exception_exit_1;
    }


    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;
    frame_exception_exit_1:


    if (exception_tb == NULL) {
        exception_tb = MAKE_TRACEBACK(frame_30c9aaa654910caf6b84f64746df29d8, exception_lineno);
    } else if (exception_tb->tb_frame != &frame_30c9aaa654910caf6b84f64746df29d8->m_frame) {
        exception_tb = ADD_TRACEBACK(exception_tb, frame_30c9aaa654910caf6b84f64746df29d8, exception_lineno);
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_30c9aaa654910caf6b84f64746df29d8,
        type_description_1,
        par_self,
        par_token,
        par_request,
        par_args,
        par_kwargs
    );


    // Release cached frame if used for exception.
    if (frame_30c9aaa654910caf6b84f64746df29d8 == cache_frame_30c9aaa654910caf6b84f64746df29d8) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_30c9aaa654910caf6b84f64746df29d8);
        cache_frame_30c9aaa654910caf6b84f64746df29d8 = NULL;
    }

    assertFrameObject(frame_30c9aaa654910caf6b84f64746df29d8);

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto function_exception_exit;
    frame_no_exception_1:;

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_token);
    Py_DECREF(par_token);
    CHECK_OBJECT(par_request);
    Py_DECREF(par_request);
    CHECK_OBJECT(par_args);
    Py_DECREF(par_args);
    CHECK_OBJECT(par_kwargs);
    Py_DECREF(par_kwargs);
    assert(exception_type);
    RESTORE_ERROR_OCCURRED(exception_type, exception_value, exception_tb);

    return NULL;

}


static PyObject *impl_oauthlib$oauth2$rfc6749$request_validator$$$function__16_validate_bearer_token(struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_self = python_pars[0];
    PyObject *par_token = python_pars[1];
    PyObject *par_scopes = python_pars[2];
    PyObject *par_request = python_pars[3];
    struct Nuitka_FrameObject *frame_4ab337411e6dd7f76096474107aada62;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    static struct Nuitka_FrameObject *cache_frame_4ab337411e6dd7f76096474107aada62 = NULL;

    // Actual function body.
    if (isFrameUnusable(cache_frame_4ab337411e6dd7f76096474107aada62)) {
        Py_XDECREF(cache_frame_4ab337411e6dd7f76096474107aada62);

#if _DEBUG_REFCOUNTS
        if (cache_frame_4ab337411e6dd7f76096474107aada62 == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_4ab337411e6dd7f76096474107aada62 = MAKE_FUNCTION_FRAME(codeobj_4ab337411e6dd7f76096474107aada62, module_oauthlib$oauth2$rfc6749$request_validator, sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_4ab337411e6dd7f76096474107aada62->m_type_description == NULL);
    frame_4ab337411e6dd7f76096474107aada62 = cache_frame_4ab337411e6dd7f76096474107aada62;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(frame_4ab337411e6dd7f76096474107aada62);
    assert(Py_REFCNT(frame_4ab337411e6dd7f76096474107aada62) == 2);

    // Framed code:
    {
        PyObject *tmp_raise_type_1;
        PyObject *tmp_make_exception_arg_1;
        tmp_make_exception_arg_1 = mod_consts[0];
        frame_4ab337411e6dd7f76096474107aada62->m_frame.f_lineno = 417;
        tmp_raise_type_1 = CALL_FUNCTION_WITH_SINGLE_ARG(PyExc_NotImplementedError, tmp_make_exception_arg_1);
        assert(!(tmp_raise_type_1 == NULL));
        exception_type = tmp_raise_type_1;
        exception_lineno = 417;
        RAISE_EXCEPTION_WITH_TYPE(&exception_type, &exception_value, &exception_tb);
        type_description_1 = "oooo";
        goto frame_exception_exit_1;
    }


    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;
    frame_exception_exit_1:


    if (exception_tb == NULL) {
        exception_tb = MAKE_TRACEBACK(frame_4ab337411e6dd7f76096474107aada62, exception_lineno);
    } else if (exception_tb->tb_frame != &frame_4ab337411e6dd7f76096474107aada62->m_frame) {
        exception_tb = ADD_TRACEBACK(exception_tb, frame_4ab337411e6dd7f76096474107aada62, exception_lineno);
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_4ab337411e6dd7f76096474107aada62,
        type_description_1,
        par_self,
        par_token,
        par_scopes,
        par_request
    );


    // Release cached frame if used for exception.
    if (frame_4ab337411e6dd7f76096474107aada62 == cache_frame_4ab337411e6dd7f76096474107aada62) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_4ab337411e6dd7f76096474107aada62);
        cache_frame_4ab337411e6dd7f76096474107aada62 = NULL;
    }

    assertFrameObject(frame_4ab337411e6dd7f76096474107aada62);

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto function_exception_exit;
    frame_no_exception_1:;

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_token);
    Py_DECREF(par_token);
    CHECK_OBJECT(par_scopes);
    Py_DECREF(par_scopes);
    CHECK_OBJECT(par_request);
    Py_DECREF(par_request);
    assert(exception_type);
    RESTORE_ERROR_OCCURRED(exception_type, exception_value, exception_tb);

    return NULL;

}


static PyObject *impl_oauthlib$oauth2$rfc6749$request_validator$$$function__17_validate_client_id(struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_self = python_pars[0];
    PyObject *par_client_id = python_pars[1];
    PyObject *par_request = python_pars[2];
    PyObject *par_args = python_pars[3];
    PyObject *par_kwargs = python_pars[4];
    struct Nuitka_FrameObject *frame_538ba625ac81714084cc16afd96934c9;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    static struct Nuitka_FrameObject *cache_frame_538ba625ac81714084cc16afd96934c9 = NULL;

    // Actual function body.
    if (isFrameUnusable(cache_frame_538ba625ac81714084cc16afd96934c9)) {
        Py_XDECREF(cache_frame_538ba625ac81714084cc16afd96934c9);

#if _DEBUG_REFCOUNTS
        if (cache_frame_538ba625ac81714084cc16afd96934c9 == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_538ba625ac81714084cc16afd96934c9 = MAKE_FUNCTION_FRAME(codeobj_538ba625ac81714084cc16afd96934c9, module_oauthlib$oauth2$rfc6749$request_validator, sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_538ba625ac81714084cc16afd96934c9->m_type_description == NULL);
    frame_538ba625ac81714084cc16afd96934c9 = cache_frame_538ba625ac81714084cc16afd96934c9;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(frame_538ba625ac81714084cc16afd96934c9);
    assert(Py_REFCNT(frame_538ba625ac81714084cc16afd96934c9) == 2);

    // Framed code:
    {
        PyObject *tmp_raise_type_1;
        PyObject *tmp_make_exception_arg_1;
        tmp_make_exception_arg_1 = mod_consts[0];
        frame_538ba625ac81714084cc16afd96934c9->m_frame.f_lineno = 435;
        tmp_raise_type_1 = CALL_FUNCTION_WITH_SINGLE_ARG(PyExc_NotImplementedError, tmp_make_exception_arg_1);
        assert(!(tmp_raise_type_1 == NULL));
        exception_type = tmp_raise_type_1;
        exception_lineno = 435;
        RAISE_EXCEPTION_WITH_TYPE(&exception_type, &exception_value, &exception_tb);
        type_description_1 = "ooooo";
        goto frame_exception_exit_1;
    }


    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;
    frame_exception_exit_1:


    if (exception_tb == NULL) {
        exception_tb = MAKE_TRACEBACK(frame_538ba625ac81714084cc16afd96934c9, exception_lineno);
    } else if (exception_tb->tb_frame != &frame_538ba625ac81714084cc16afd96934c9->m_frame) {
        exception_tb = ADD_TRACEBACK(exception_tb, frame_538ba625ac81714084cc16afd96934c9, exception_lineno);
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_538ba625ac81714084cc16afd96934c9,
        type_description_1,
        par_self,
        par_client_id,
        par_request,
        par_args,
        par_kwargs
    );


    // Release cached frame if used for exception.
    if (frame_538ba625ac81714084cc16afd96934c9 == cache_frame_538ba625ac81714084cc16afd96934c9) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_538ba625ac81714084cc16afd96934c9);
        cache_frame_538ba625ac81714084cc16afd96934c9 = NULL;
    }

    assertFrameObject(frame_538ba625ac81714084cc16afd96934c9);

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto function_exception_exit;
    frame_no_exception_1:;

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_client_id);
    Py_DECREF(par_client_id);
    CHECK_OBJECT(par_request);
    Py_DECREF(par_request);
    CHECK_OBJECT(par_args);
    Py_DECREF(par_args);
    CHECK_OBJECT(par_kwargs);
    Py_DECREF(par_kwargs);
    assert(exception_type);
    RESTORE_ERROR_OCCURRED(exception_type, exception_value, exception_tb);

    return NULL;

}


static PyObject *impl_oauthlib$oauth2$rfc6749$request_validator$$$function__18_validate_code(struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_self = python_pars[0];
    PyObject *par_client_id = python_pars[1];
    PyObject *par_code = python_pars[2];
    PyObject *par_client = python_pars[3];
    PyObject *par_request = python_pars[4];
    PyObject *par_args = python_pars[5];
    PyObject *par_kwargs = python_pars[6];
    struct Nuitka_FrameObject *frame_22929cfc4badf0d11a356027b016beba;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    static struct Nuitka_FrameObject *cache_frame_22929cfc4badf0d11a356027b016beba = NULL;

    // Actual function body.
    if (isFrameUnusable(cache_frame_22929cfc4badf0d11a356027b016beba)) {
        Py_XDECREF(cache_frame_22929cfc4badf0d11a356027b016beba);

#if _DEBUG_REFCOUNTS
        if (cache_frame_22929cfc4badf0d11a356027b016beba == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_22929cfc4badf0d11a356027b016beba = MAKE_FUNCTION_FRAME(codeobj_22929cfc4badf0d11a356027b016beba, module_oauthlib$oauth2$rfc6749$request_validator, sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_22929cfc4badf0d11a356027b016beba->m_type_description == NULL);
    frame_22929cfc4badf0d11a356027b016beba = cache_frame_22929cfc4badf0d11a356027b016beba;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(frame_22929cfc4badf0d11a356027b016beba);
    assert(Py_REFCNT(frame_22929cfc4badf0d11a356027b016beba) == 2);

    // Framed code:
    {
        PyObject *tmp_raise_type_1;
        PyObject *tmp_make_exception_arg_1;
        tmp_make_exception_arg_1 = mod_consts[0];
        frame_22929cfc4badf0d11a356027b016beba->m_frame.f_lineno = 470;
        tmp_raise_type_1 = CALL_FUNCTION_WITH_SINGLE_ARG(PyExc_NotImplementedError, tmp_make_exception_arg_1);
        assert(!(tmp_raise_type_1 == NULL));
        exception_type = tmp_raise_type_1;
        exception_lineno = 470;
        RAISE_EXCEPTION_WITH_TYPE(&exception_type, &exception_value, &exception_tb);
        type_description_1 = "ooooooo";
        goto frame_exception_exit_1;
    }


    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;
    frame_exception_exit_1:


    if (exception_tb == NULL) {
        exception_tb = MAKE_TRACEBACK(frame_22929cfc4badf0d11a356027b016beba, exception_lineno);
    } else if (exception_tb->tb_frame != &frame_22929cfc4badf0d11a356027b016beba->m_frame) {
        exception_tb = ADD_TRACEBACK(exception_tb, frame_22929cfc4badf0d11a356027b016beba, exception_lineno);
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_22929cfc4badf0d11a356027b016beba,
        type_description_1,
        par_self,
        par_client_id,
        par_code,
        par_client,
        par_request,
        par_args,
        par_kwargs
    );


    // Release cached frame if used for exception.
    if (frame_22929cfc4badf0d11a356027b016beba == cache_frame_22929cfc4badf0d11a356027b016beba) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_22929cfc4badf0d11a356027b016beba);
        cache_frame_22929cfc4badf0d11a356027b016beba = NULL;
    }

    assertFrameObject(frame_22929cfc4badf0d11a356027b016beba);

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto function_exception_exit;
    frame_no_exception_1:;

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_client_id);
    Py_DECREF(par_client_id);
    CHECK_OBJECT(par_code);
    Py_DECREF(par_code);
    CHECK_OBJECT(par_client);
    Py_DECREF(par_client);
    CHECK_OBJECT(par_request);
    Py_DECREF(par_request);
    CHECK_OBJECT(par_args);
    Py_DECREF(par_args);
    CHECK_OBJECT(par_kwargs);
    Py_DECREF(par_kwargs);
    assert(exception_type);
    RESTORE_ERROR_OCCURRED(exception_type, exception_value, exception_tb);

    return NULL;

}


static PyObject *impl_oauthlib$oauth2$rfc6749$request_validator$$$function__19_validate_grant_type(struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_self = python_pars[0];
    PyObject *par_client_id = python_pars[1];
    PyObject *par_grant_type = python_pars[2];
    PyObject *par_client = python_pars[3];
    PyObject *par_request = python_pars[4];
    PyObject *par_args = python_pars[5];
    PyObject *par_kwargs = python_pars[6];
    struct Nuitka_FrameObject *frame_770e7fbf1d2d8bd6051ac5649e1d0dc2;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    static struct Nuitka_FrameObject *cache_frame_770e7fbf1d2d8bd6051ac5649e1d0dc2 = NULL;

    // Actual function body.
    if (isFrameUnusable(cache_frame_770e7fbf1d2d8bd6051ac5649e1d0dc2)) {
        Py_XDECREF(cache_frame_770e7fbf1d2d8bd6051ac5649e1d0dc2);

#if _DEBUG_REFCOUNTS
        if (cache_frame_770e7fbf1d2d8bd6051ac5649e1d0dc2 == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_770e7fbf1d2d8bd6051ac5649e1d0dc2 = MAKE_FUNCTION_FRAME(codeobj_770e7fbf1d2d8bd6051ac5649e1d0dc2, module_oauthlib$oauth2$rfc6749$request_validator, sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_770e7fbf1d2d8bd6051ac5649e1d0dc2->m_type_description == NULL);
    frame_770e7fbf1d2d8bd6051ac5649e1d0dc2 = cache_frame_770e7fbf1d2d8bd6051ac5649e1d0dc2;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(frame_770e7fbf1d2d8bd6051ac5649e1d0dc2);
    assert(Py_REFCNT(frame_770e7fbf1d2d8bd6051ac5649e1d0dc2) == 2);

    // Framed code:
    {
        PyObject *tmp_raise_type_1;
        PyObject *tmp_make_exception_arg_1;
        tmp_make_exception_arg_1 = mod_consts[0];
        frame_770e7fbf1d2d8bd6051ac5649e1d0dc2->m_frame.f_lineno = 488;
        tmp_raise_type_1 = CALL_FUNCTION_WITH_SINGLE_ARG(PyExc_NotImplementedError, tmp_make_exception_arg_1);
        assert(!(tmp_raise_type_1 == NULL));
        exception_type = tmp_raise_type_1;
        exception_lineno = 488;
        RAISE_EXCEPTION_WITH_TYPE(&exception_type, &exception_value, &exception_tb);
        type_description_1 = "ooooooo";
        goto frame_exception_exit_1;
    }


    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;
    frame_exception_exit_1:


    if (exception_tb == NULL) {
        exception_tb = MAKE_TRACEBACK(frame_770e7fbf1d2d8bd6051ac5649e1d0dc2, exception_lineno);
    } else if (exception_tb->tb_frame != &frame_770e7fbf1d2d8bd6051ac5649e1d0dc2->m_frame) {
        exception_tb = ADD_TRACEBACK(exception_tb, frame_770e7fbf1d2d8bd6051ac5649e1d0dc2, exception_lineno);
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_770e7fbf1d2d8bd6051ac5649e1d0dc2,
        type_description_1,
        par_self,
        par_client_id,
        par_grant_type,
        par_client,
        par_request,
        par_args,
        par_kwargs
    );


    // Release cached frame if used for exception.
    if (frame_770e7fbf1d2d8bd6051ac5649e1d0dc2 == cache_frame_770e7fbf1d2d8bd6051ac5649e1d0dc2) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_770e7fbf1d2d8bd6051ac5649e1d0dc2);
        cache_frame_770e7fbf1d2d8bd6051ac5649e1d0dc2 = NULL;
    }

    assertFrameObject(frame_770e7fbf1d2d8bd6051ac5649e1d0dc2);

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto function_exception_exit;
    frame_no_exception_1:;

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_client_id);
    Py_DECREF(par_client_id);
    CHECK_OBJECT(par_grant_type);
    Py_DECREF(par_grant_type);
    CHECK_OBJECT(par_client);
    Py_DECREF(par_client);
    CHECK_OBJECT(par_request);
    Py_DECREF(par_request);
    CHECK_OBJECT(par_args);
    Py_DECREF(par_args);
    CHECK_OBJECT(par_kwargs);
    Py_DECREF(par_kwargs);
    assert(exception_type);
    RESTORE_ERROR_OCCURRED(exception_type, exception_value, exception_tb);

    return NULL;

}


static PyObject *impl_oauthlib$oauth2$rfc6749$request_validator$$$function__20_validate_redirect_uri(struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_self = python_pars[0];
    PyObject *par_client_id = python_pars[1];
    PyObject *par_redirect_uri = python_pars[2];
    PyObject *par_request = python_pars[3];
    PyObject *par_args = python_pars[4];
    PyObject *par_kwargs = python_pars[5];
    struct Nuitka_FrameObject *frame_b3675bb61cf0f9b19c800807c4973f4b;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    static struct Nuitka_FrameObject *cache_frame_b3675bb61cf0f9b19c800807c4973f4b = NULL;

    // Actual function body.
    if (isFrameUnusable(cache_frame_b3675bb61cf0f9b19c800807c4973f4b)) {
        Py_XDECREF(cache_frame_b3675bb61cf0f9b19c800807c4973f4b);

#if _DEBUG_REFCOUNTS
        if (cache_frame_b3675bb61cf0f9b19c800807c4973f4b == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_b3675bb61cf0f9b19c800807c4973f4b = MAKE_FUNCTION_FRAME(codeobj_b3675bb61cf0f9b19c800807c4973f4b, module_oauthlib$oauth2$rfc6749$request_validator, sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_b3675bb61cf0f9b19c800807c4973f4b->m_type_description == NULL);
    frame_b3675bb61cf0f9b19c800807c4973f4b = cache_frame_b3675bb61cf0f9b19c800807c4973f4b;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(frame_b3675bb61cf0f9b19c800807c4973f4b);
    assert(Py_REFCNT(frame_b3675bb61cf0f9b19c800807c4973f4b) == 2);

    // Framed code:
    {
        PyObject *tmp_raise_type_1;
        PyObject *tmp_make_exception_arg_1;
        tmp_make_exception_arg_1 = mod_consts[0];
        frame_b3675bb61cf0f9b19c800807c4973f4b->m_frame.f_lineno = 506;
        tmp_raise_type_1 = CALL_FUNCTION_WITH_SINGLE_ARG(PyExc_NotImplementedError, tmp_make_exception_arg_1);
        assert(!(tmp_raise_type_1 == NULL));
        exception_type = tmp_raise_type_1;
        exception_lineno = 506;
        RAISE_EXCEPTION_WITH_TYPE(&exception_type, &exception_value, &exception_tb);
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }


    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;
    frame_exception_exit_1:


    if (exception_tb == NULL) {
        exception_tb = MAKE_TRACEBACK(frame_b3675bb61cf0f9b19c800807c4973f4b, exception_lineno);
    } else if (exception_tb->tb_frame != &frame_b3675bb61cf0f9b19c800807c4973f4b->m_frame) {
        exception_tb = ADD_TRACEBACK(exception_tb, frame_b3675bb61cf0f9b19c800807c4973f4b, exception_lineno);
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_b3675bb61cf0f9b19c800807c4973f4b,
        type_description_1,
        par_self,
        par_client_id,
        par_redirect_uri,
        par_request,
        par_args,
        par_kwargs
    );


    // Release cached frame if used for exception.
    if (frame_b3675bb61cf0f9b19c800807c4973f4b == cache_frame_b3675bb61cf0f9b19c800807c4973f4b) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_b3675bb61cf0f9b19c800807c4973f4b);
        cache_frame_b3675bb61cf0f9b19c800807c4973f4b = NULL;
    }

    assertFrameObject(frame_b3675bb61cf0f9b19c800807c4973f4b);

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto function_exception_exit;
    frame_no_exception_1:;

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_client_id);
    Py_DECREF(par_client_id);
    CHECK_OBJECT(par_redirect_uri);
    Py_DECREF(par_redirect_uri);
    CHECK_OBJECT(par_request);
    Py_DECREF(par_request);
    CHECK_OBJECT(par_args);
    Py_DECREF(par_args);
    CHECK_OBJECT(par_kwargs);
    Py_DECREF(par_kwargs);
    assert(exception_type);
    RESTORE_ERROR_OCCURRED(exception_type, exception_value, exception_tb);

    return NULL;

}


static PyObject *impl_oauthlib$oauth2$rfc6749$request_validator$$$function__21_validate_refresh_token(struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_self = python_pars[0];
    PyObject *par_refresh_token = python_pars[1];
    PyObject *par_client = python_pars[2];
    PyObject *par_request = python_pars[3];
    PyObject *par_args = python_pars[4];
    PyObject *par_kwargs = python_pars[5];
    struct Nuitka_FrameObject *frame_3e7b33e54320d6baa5b70180221efaf4;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    static struct Nuitka_FrameObject *cache_frame_3e7b33e54320d6baa5b70180221efaf4 = NULL;

    // Actual function body.
    if (isFrameUnusable(cache_frame_3e7b33e54320d6baa5b70180221efaf4)) {
        Py_XDECREF(cache_frame_3e7b33e54320d6baa5b70180221efaf4);

#if _DEBUG_REFCOUNTS
        if (cache_frame_3e7b33e54320d6baa5b70180221efaf4 == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_3e7b33e54320d6baa5b70180221efaf4 = MAKE_FUNCTION_FRAME(codeobj_3e7b33e54320d6baa5b70180221efaf4, module_oauthlib$oauth2$rfc6749$request_validator, sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_3e7b33e54320d6baa5b70180221efaf4->m_type_description == NULL);
    frame_3e7b33e54320d6baa5b70180221efaf4 = cache_frame_3e7b33e54320d6baa5b70180221efaf4;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(frame_3e7b33e54320d6baa5b70180221efaf4);
    assert(Py_REFCNT(frame_3e7b33e54320d6baa5b70180221efaf4) == 2);

    // Framed code:
    {
        PyObject *tmp_raise_type_1;
        PyObject *tmp_make_exception_arg_1;
        tmp_make_exception_arg_1 = mod_consts[0];
        frame_3e7b33e54320d6baa5b70180221efaf4->m_frame.f_lineno = 525;
        tmp_raise_type_1 = CALL_FUNCTION_WITH_SINGLE_ARG(PyExc_NotImplementedError, tmp_make_exception_arg_1);
        assert(!(tmp_raise_type_1 == NULL));
        exception_type = tmp_raise_type_1;
        exception_lineno = 525;
        RAISE_EXCEPTION_WITH_TYPE(&exception_type, &exception_value, &exception_tb);
        type_description_1 = "oooooo";
        goto frame_exception_exit_1;
    }


    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;
    frame_exception_exit_1:


    if (exception_tb == NULL) {
        exception_tb = MAKE_TRACEBACK(frame_3e7b33e54320d6baa5b70180221efaf4, exception_lineno);
    } else if (exception_tb->tb_frame != &frame_3e7b33e54320d6baa5b70180221efaf4->m_frame) {
        exception_tb = ADD_TRACEBACK(exception_tb, frame_3e7b33e54320d6baa5b70180221efaf4, exception_lineno);
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_3e7b33e54320d6baa5b70180221efaf4,
        type_description_1,
        par_self,
        par_refresh_token,
        par_client,
        par_request,
        par_args,
        par_kwargs
    );


    // Release cached frame if used for exception.
    if (frame_3e7b33e54320d6baa5b70180221efaf4 == cache_frame_3e7b33e54320d6baa5b70180221efaf4) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_3e7b33e54320d6baa5b70180221efaf4);
        cache_frame_3e7b33e54320d6baa5b70180221efaf4 = NULL;
    }

    assertFrameObject(frame_3e7b33e54320d6baa5b70180221efaf4);

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto function_exception_exit;
    frame_no_exception_1:;

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_refresh_token);
    Py_DECREF(par_refresh_token);
    CHECK_OBJECT(par_client);
    Py_DECREF(par_client);
    CHECK_OBJECT(par_request);
    Py_DECREF(par_request);
    CHECK_OBJECT(par_args);
    Py_DECREF(par_args);
    CHECK_OBJECT(par_kwargs);
    Py_DECREF(par_kwargs);
    assert(exception_type);
    RESTORE_ERROR_OCCURRED(exception_type, exception_value, exception_tb);

    return NULL;

}


static PyObject *impl_oauthlib$oauth2$rfc6749$request_validator$$$function__22_validate_response_type(struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_self = python_pars[0];
    PyObject *par_client_id = python_pars[1];
    PyObject *par_response_type = python_pars[2];
    PyObject *par_client = python_pars[3];
    PyObject *par_request = python_pars[4];
    PyObject *par_args = python_pars[5];
    PyObject *par_kwargs = python_pars[6];
    struct Nuitka_FrameObject *frame_35e4dba3786838d11c6792c05107d109;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    static struct Nuitka_FrameObject *cache_frame_35e4dba3786838d11c6792c05107d109 = NULL;

    // Actual function body.
    if (isFrameUnusable(cache_frame_35e4dba3786838d11c6792c05107d109)) {
        Py_XDECREF(cache_frame_35e4dba3786838d11c6792c05107d109);

#if _DEBUG_REFCOUNTS
        if (cache_frame_35e4dba3786838d11c6792c05107d109 == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_35e4dba3786838d11c6792c05107d109 = MAKE_FUNCTION_FRAME(codeobj_35e4dba3786838d11c6792c05107d109, module_oauthlib$oauth2$rfc6749$request_validator, sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_35e4dba3786838d11c6792c05107d109->m_type_description == NULL);
    frame_35e4dba3786838d11c6792c05107d109 = cache_frame_35e4dba3786838d11c6792c05107d109;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(frame_35e4dba3786838d11c6792c05107d109);
    assert(Py_REFCNT(frame_35e4dba3786838d11c6792c05107d109) == 2);

    // Framed code:
    {
        PyObject *tmp_raise_type_1;
        PyObject *tmp_make_exception_arg_1;
        tmp_make_exception_arg_1 = mod_consts[0];
        frame_35e4dba3786838d11c6792c05107d109->m_frame.f_lineno = 541;
        tmp_raise_type_1 = CALL_FUNCTION_WITH_SINGLE_ARG(PyExc_NotImplementedError, tmp_make_exception_arg_1);
        assert(!(tmp_raise_type_1 == NULL));
        exception_type = tmp_raise_type_1;
        exception_lineno = 541;
        RAISE_EXCEPTION_WITH_TYPE(&exception_type, &exception_value, &exception_tb);
        type_description_1 = "ooooooo";
        goto frame_exception_exit_1;
    }


    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;
    frame_exception_exit_1:


    if (exception_tb == NULL) {
        exception_tb = MAKE_TRACEBACK(frame_35e4dba3786838d11c6792c05107d109, exception_lineno);
    } else if (exception_tb->tb_frame != &frame_35e4dba3786838d11c6792c05107d109->m_frame) {
        exception_tb = ADD_TRACEBACK(exception_tb, frame_35e4dba3786838d11c6792c05107d109, exception_lineno);
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_35e4dba3786838d11c6792c05107d109,
        type_description_1,
        par_self,
        par_client_id,
        par_response_type,
        par_client,
        par_request,
        par_args,
        par_kwargs
    );


    // Release cached frame if used for exception.
    if (frame_35e4dba3786838d11c6792c05107d109 == cache_frame_35e4dba3786838d11c6792c05107d109) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_35e4dba3786838d11c6792c05107d109);
        cache_frame_35e4dba3786838d11c6792c05107d109 = NULL;
    }

    assertFrameObject(frame_35e4dba3786838d11c6792c05107d109);

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto function_exception_exit;
    frame_no_exception_1:;

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_client_id);
    Py_DECREF(par_client_id);
    CHECK_OBJECT(par_response_type);
    Py_DECREF(par_response_type);
    CHECK_OBJECT(par_client);
    Py_DECREF(par_client);
    CHECK_OBJECT(par_request);
    Py_DECREF(par_request);
    CHECK_OBJECT(par_args);
    Py_DECREF(par_args);
    CHECK_OBJECT(par_kwargs);
    Py_DECREF(par_kwargs);
    assert(exception_type);
    RESTORE_ERROR_OCCURRED(exception_type, exception_value, exception_tb);

    return NULL;

}


static PyObject *impl_oauthlib$oauth2$rfc6749$request_validator$$$function__23_validate_scopes(struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_self = python_pars[0];
    PyObject *par_client_id = python_pars[1];
    PyObject *par_scopes = python_pars[2];
    PyObject *par_client = python_pars[3];
    PyObject *par_request = python_pars[4];
    PyObject *par_args = python_pars[5];
    PyObject *par_kwargs = python_pars[6];
    struct Nuitka_FrameObject *frame_489b9d905bb815d7f1578d1548e010e5;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    static struct Nuitka_FrameObject *cache_frame_489b9d905bb815d7f1578d1548e010e5 = NULL;

    // Actual function body.
    if (isFrameUnusable(cache_frame_489b9d905bb815d7f1578d1548e010e5)) {
        Py_XDECREF(cache_frame_489b9d905bb815d7f1578d1548e010e5);

#if _DEBUG_REFCOUNTS
        if (cache_frame_489b9d905bb815d7f1578d1548e010e5 == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_489b9d905bb815d7f1578d1548e010e5 = MAKE_FUNCTION_FRAME(codeobj_489b9d905bb815d7f1578d1548e010e5, module_oauthlib$oauth2$rfc6749$request_validator, sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_489b9d905bb815d7f1578d1548e010e5->m_type_description == NULL);
    frame_489b9d905bb815d7f1578d1548e010e5 = cache_frame_489b9d905bb815d7f1578d1548e010e5;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(frame_489b9d905bb815d7f1578d1548e010e5);
    assert(Py_REFCNT(frame_489b9d905bb815d7f1578d1548e010e5) == 2);

    // Framed code:
    {
        PyObject *tmp_raise_type_1;
        PyObject *tmp_make_exception_arg_1;
        tmp_make_exception_arg_1 = mod_consts[0];
        frame_489b9d905bb815d7f1578d1548e010e5->m_frame.f_lineno = 559;
        tmp_raise_type_1 = CALL_FUNCTION_WITH_SINGLE_ARG(PyExc_NotImplementedError, tmp_make_exception_arg_1);
        assert(!(tmp_raise_type_1 == NULL));
        exception_type = tmp_raise_type_1;
        exception_lineno = 559;
        RAISE_EXCEPTION_WITH_TYPE(&exception_type, &exception_value, &exception_tb);
        type_description_1 = "ooooooo";
        goto frame_exception_exit_1;
    }


    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;
    frame_exception_exit_1:


    if (exception_tb == NULL) {
        exception_tb = MAKE_TRACEBACK(frame_489b9d905bb815d7f1578d1548e010e5, exception_lineno);
    } else if (exception_tb->tb_frame != &frame_489b9d905bb815d7f1578d1548e010e5->m_frame) {
        exception_tb = ADD_TRACEBACK(exception_tb, frame_489b9d905bb815d7f1578d1548e010e5, exception_lineno);
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_489b9d905bb815d7f1578d1548e010e5,
        type_description_1,
        par_self,
        par_client_id,
        par_scopes,
        par_client,
        par_request,
        par_args,
        par_kwargs
    );


    // Release cached frame if used for exception.
    if (frame_489b9d905bb815d7f1578d1548e010e5 == cache_frame_489b9d905bb815d7f1578d1548e010e5) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_489b9d905bb815d7f1578d1548e010e5);
        cache_frame_489b9d905bb815d7f1578d1548e010e5 = NULL;
    }

    assertFrameObject(frame_489b9d905bb815d7f1578d1548e010e5);

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto function_exception_exit;
    frame_no_exception_1:;

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_client_id);
    Py_DECREF(par_client_id);
    CHECK_OBJECT(par_scopes);
    Py_DECREF(par_scopes);
    CHECK_OBJECT(par_client);
    Py_DECREF(par_client);
    CHECK_OBJECT(par_request);
    Py_DECREF(par_request);
    CHECK_OBJECT(par_args);
    Py_DECREF(par_args);
    CHECK_OBJECT(par_kwargs);
    Py_DECREF(par_kwargs);
    assert(exception_type);
    RESTORE_ERROR_OCCURRED(exception_type, exception_value, exception_tb);

    return NULL;

}


static PyObject *impl_oauthlib$oauth2$rfc6749$request_validator$$$function__24_validate_user(struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_self = python_pars[0];
    PyObject *par_username = python_pars[1];
    PyObject *par_password = python_pars[2];
    PyObject *par_client = python_pars[3];
    PyObject *par_request = python_pars[4];
    PyObject *par_args = python_pars[5];
    PyObject *par_kwargs = python_pars[6];
    struct Nuitka_FrameObject *frame_99168fe18391008f5fa4fc4155dd7815;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    static struct Nuitka_FrameObject *cache_frame_99168fe18391008f5fa4fc4155dd7815 = NULL;

    // Actual function body.
    if (isFrameUnusable(cache_frame_99168fe18391008f5fa4fc4155dd7815)) {
        Py_XDECREF(cache_frame_99168fe18391008f5fa4fc4155dd7815);

#if _DEBUG_REFCOUNTS
        if (cache_frame_99168fe18391008f5fa4fc4155dd7815 == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_99168fe18391008f5fa4fc4155dd7815 = MAKE_FUNCTION_FRAME(codeobj_99168fe18391008f5fa4fc4155dd7815, module_oauthlib$oauth2$rfc6749$request_validator, sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_99168fe18391008f5fa4fc4155dd7815->m_type_description == NULL);
    frame_99168fe18391008f5fa4fc4155dd7815 = cache_frame_99168fe18391008f5fa4fc4155dd7815;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(frame_99168fe18391008f5fa4fc4155dd7815);
    assert(Py_REFCNT(frame_99168fe18391008f5fa4fc4155dd7815) == 2);

    // Framed code:
    {
        PyObject *tmp_raise_type_1;
        PyObject *tmp_make_exception_arg_1;
        tmp_make_exception_arg_1 = mod_consts[0];
        frame_99168fe18391008f5fa4fc4155dd7815->m_frame.f_lineno = 579;
        tmp_raise_type_1 = CALL_FUNCTION_WITH_SINGLE_ARG(PyExc_NotImplementedError, tmp_make_exception_arg_1);
        assert(!(tmp_raise_type_1 == NULL));
        exception_type = tmp_raise_type_1;
        exception_lineno = 579;
        RAISE_EXCEPTION_WITH_TYPE(&exception_type, &exception_value, &exception_tb);
        type_description_1 = "ooooooo";
        goto frame_exception_exit_1;
    }


    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;
    frame_exception_exit_1:


    if (exception_tb == NULL) {
        exception_tb = MAKE_TRACEBACK(frame_99168fe18391008f5fa4fc4155dd7815, exception_lineno);
    } else if (exception_tb->tb_frame != &frame_99168fe18391008f5fa4fc4155dd7815->m_frame) {
        exception_tb = ADD_TRACEBACK(exception_tb, frame_99168fe18391008f5fa4fc4155dd7815, exception_lineno);
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_99168fe18391008f5fa4fc4155dd7815,
        type_description_1,
        par_self,
        par_username,
        par_password,
        par_client,
        par_request,
        par_args,
        par_kwargs
    );


    // Release cached frame if used for exception.
    if (frame_99168fe18391008f5fa4fc4155dd7815 == cache_frame_99168fe18391008f5fa4fc4155dd7815) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_99168fe18391008f5fa4fc4155dd7815);
        cache_frame_99168fe18391008f5fa4fc4155dd7815 = NULL;
    }

    assertFrameObject(frame_99168fe18391008f5fa4fc4155dd7815);

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto function_exception_exit;
    frame_no_exception_1:;

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_username);
    Py_DECREF(par_username);
    CHECK_OBJECT(par_password);
    Py_DECREF(par_password);
    CHECK_OBJECT(par_client);
    Py_DECREF(par_client);
    CHECK_OBJECT(par_request);
    Py_DECREF(par_request);
    CHECK_OBJECT(par_args);
    Py_DECREF(par_args);
    CHECK_OBJECT(par_kwargs);
    Py_DECREF(par_kwargs);
    assert(exception_type);
    RESTORE_ERROR_OCCURRED(exception_type, exception_value, exception_tb);

    return NULL;

}


static PyObject *impl_oauthlib$oauth2$rfc6749$request_validator$$$function__27_get_code_challenge_method(struct Nuitka_FunctionObject const *self, PyObject **python_pars) {
    // Preserve error status for checks
#ifndef __NUITKA_NO_ASSERT__
    NUITKA_MAY_BE_UNUSED bool had_error = ERROR_OCCURRED();
#endif

    // Local variable declarations.
    PyObject *par_self = python_pars[0];
    PyObject *par_code = python_pars[1];
    PyObject *par_request = python_pars[2];
    struct Nuitka_FrameObject *frame_ba068dbaf8b68cb9c006b9ee06af5e58;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    static struct Nuitka_FrameObject *cache_frame_ba068dbaf8b68cb9c006b9ee06af5e58 = NULL;

    // Actual function body.
    if (isFrameUnusable(cache_frame_ba068dbaf8b68cb9c006b9ee06af5e58)) {
        Py_XDECREF(cache_frame_ba068dbaf8b68cb9c006b9ee06af5e58);

#if _DEBUG_REFCOUNTS
        if (cache_frame_ba068dbaf8b68cb9c006b9ee06af5e58 == NULL) {
            count_active_frame_cache_instances += 1;
        } else {
            count_released_frame_cache_instances += 1;
        }
        count_allocated_frame_cache_instances += 1;
#endif
        cache_frame_ba068dbaf8b68cb9c006b9ee06af5e58 = MAKE_FUNCTION_FRAME(codeobj_ba068dbaf8b68cb9c006b9ee06af5e58, module_oauthlib$oauth2$rfc6749$request_validator, sizeof(void *)+sizeof(void *)+sizeof(void *));
#if _DEBUG_REFCOUNTS
    } else {
        count_hit_frame_cache_instances += 1;
#endif
    }

    assert(cache_frame_ba068dbaf8b68cb9c006b9ee06af5e58->m_type_description == NULL);
    frame_ba068dbaf8b68cb9c006b9ee06af5e58 = cache_frame_ba068dbaf8b68cb9c006b9ee06af5e58;

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(frame_ba068dbaf8b68cb9c006b9ee06af5e58);
    assert(Py_REFCNT(frame_ba068dbaf8b68cb9c006b9ee06af5e58) == 2);

    // Framed code:
    {
        PyObject *tmp_raise_type_1;
        PyObject *tmp_make_exception_arg_1;
        tmp_make_exception_arg_1 = mod_consts[0];
        frame_ba068dbaf8b68cb9c006b9ee06af5e58->m_frame.f_lineno = 654;
        tmp_raise_type_1 = CALL_FUNCTION_WITH_SINGLE_ARG(PyExc_NotImplementedError, tmp_make_exception_arg_1);
        assert(!(tmp_raise_type_1 == NULL));
        exception_type = tmp_raise_type_1;
        exception_lineno = 654;
        RAISE_EXCEPTION_WITH_TYPE(&exception_type, &exception_value, &exception_tb);
        type_description_1 = "ooo";
        goto frame_exception_exit_1;
    }


    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;
    frame_exception_exit_1:


    if (exception_tb == NULL) {
        exception_tb = MAKE_TRACEBACK(frame_ba068dbaf8b68cb9c006b9ee06af5e58, exception_lineno);
    } else if (exception_tb->tb_frame != &frame_ba068dbaf8b68cb9c006b9ee06af5e58->m_frame) {
        exception_tb = ADD_TRACEBACK(exception_tb, frame_ba068dbaf8b68cb9c006b9ee06af5e58, exception_lineno);
    }

    // Attaches locals to frame if any.
    Nuitka_Frame_AttachLocals(
        frame_ba068dbaf8b68cb9c006b9ee06af5e58,
        type_description_1,
        par_self,
        par_code,
        par_request
    );


    // Release cached frame if used for exception.
    if (frame_ba068dbaf8b68cb9c006b9ee06af5e58 == cache_frame_ba068dbaf8b68cb9c006b9ee06af5e58) {
#if _DEBUG_REFCOUNTS
        count_active_frame_cache_instances -= 1;
        count_released_frame_cache_instances += 1;
#endif
        Py_DECREF(cache_frame_ba068dbaf8b68cb9c006b9ee06af5e58);
        cache_frame_ba068dbaf8b68cb9c006b9ee06af5e58 = NULL;
    }

    assertFrameObject(frame_ba068dbaf8b68cb9c006b9ee06af5e58);

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto function_exception_exit;
    frame_no_exception_1:;

    NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
    return NULL;

function_exception_exit:
    CHECK_OBJECT(par_self);
    Py_DECREF(par_self);
    CHECK_OBJECT(par_code);
    Py_DECREF(par_code);
    CHECK_OBJECT(par_request);
    Py_DECREF(par_request);
    assert(exception_type);
    RESTORE_ERROR_OCCURRED(exception_type, exception_value, exception_tb);

    return NULL;

}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__10_invalidate_authorization_code() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_oauthlib$oauth2$rfc6749$request_validator$$$function__10_invalidate_authorization_code,
        mod_consts[60],
#if PYTHON_VERSION >= 0x300
        mod_consts[61],
#endif
        codeobj_eb455e7e8b0726ab205bddb0b5032af7,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[8],
        NULL,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__11_revoke_token() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_oauthlib$oauth2$rfc6749$request_validator$$$function__11_revoke_token,
        mod_consts[62],
#if PYTHON_VERSION >= 0x300
        mod_consts[63],
#endif
        codeobj_88f698014760404e5103d09728eed55f,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[9],
        NULL,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__12_rotate_refresh_token() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        NULL,
        mod_consts[65],
#if PYTHON_VERSION >= 0x300
        mod_consts[66],
#endif
        codeobj_23a6ed71221ed055494325ccce6c7aff,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[64],
        NULL,
        0
    );
    Nuitka_Function_EnableConstReturnTrue(result);

    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__13_save_authorization_code() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_oauthlib$oauth2$rfc6749$request_validator$$$function__13_save_authorization_code,
        mod_consts[67],
#if PYTHON_VERSION >= 0x300
        mod_consts[68],
#endif
        codeobj_a60172c1215f2f00cf0915196d66e963,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[10],
        NULL,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__14_save_token() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_oauthlib$oauth2$rfc6749$request_validator$$$function__14_save_token,
        mod_consts[69],
#if PYTHON_VERSION >= 0x300
        mod_consts[70],
#endif
        codeobj_f6577c7b7854260253ce470c8440f149,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[12],
        NULL,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__15_save_bearer_token() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_oauthlib$oauth2$rfc6749$request_validator$$$function__15_save_bearer_token,
        mod_consts[11],
#if PYTHON_VERSION >= 0x300
        mod_consts[71],
#endif
        codeobj_30c9aaa654910caf6b84f64746df29d8,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[13],
        NULL,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__16_validate_bearer_token() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_oauthlib$oauth2$rfc6749$request_validator$$$function__16_validate_bearer_token,
        mod_consts[72],
#if PYTHON_VERSION >= 0x300
        mod_consts[73],
#endif
        codeobj_4ab337411e6dd7f76096474107aada62,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[14],
        NULL,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__17_validate_client_id() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_oauthlib$oauth2$rfc6749$request_validator$$$function__17_validate_client_id,
        mod_consts[74],
#if PYTHON_VERSION >= 0x300
        mod_consts[75],
#endif
        codeobj_538ba625ac81714084cc16afd96934c9,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[15],
        NULL,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__18_validate_code() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_oauthlib$oauth2$rfc6749$request_validator$$$function__18_validate_code,
        mod_consts[76],
#if PYTHON_VERSION >= 0x300
        mod_consts[77],
#endif
        codeobj_22929cfc4badf0d11a356027b016beba,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[16],
        NULL,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__19_validate_grant_type() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_oauthlib$oauth2$rfc6749$request_validator$$$function__19_validate_grant_type,
        mod_consts[78],
#if PYTHON_VERSION >= 0x300
        mod_consts[79],
#endif
        codeobj_770e7fbf1d2d8bd6051ac5649e1d0dc2,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[17],
        NULL,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__1_client_authentication_required() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        NULL,
        mod_consts[41],
#if PYTHON_VERSION >= 0x300
        mod_consts[42],
#endif
        codeobj_e9ca277b71c24aad2da879e1094a443c,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[40],
        NULL,
        0
    );
    Nuitka_Function_EnableConstReturnTrue(result);

    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__20_validate_redirect_uri() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_oauthlib$oauth2$rfc6749$request_validator$$$function__20_validate_redirect_uri,
        mod_consts[80],
#if PYTHON_VERSION >= 0x300
        mod_consts[81],
#endif
        codeobj_b3675bb61cf0f9b19c800807c4973f4b,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[18],
        NULL,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__21_validate_refresh_token() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_oauthlib$oauth2$rfc6749$request_validator$$$function__21_validate_refresh_token,
        mod_consts[82],
#if PYTHON_VERSION >= 0x300
        mod_consts[83],
#endif
        codeobj_3e7b33e54320d6baa5b70180221efaf4,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[19],
        NULL,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__22_validate_response_type() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_oauthlib$oauth2$rfc6749$request_validator$$$function__22_validate_response_type,
        mod_consts[84],
#if PYTHON_VERSION >= 0x300
        mod_consts[85],
#endif
        codeobj_35e4dba3786838d11c6792c05107d109,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[20],
        NULL,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__23_validate_scopes() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_oauthlib$oauth2$rfc6749$request_validator$$$function__23_validate_scopes,
        mod_consts[86],
#if PYTHON_VERSION >= 0x300
        mod_consts[87],
#endif
        codeobj_489b9d905bb815d7f1578d1548e010e5,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[21],
        NULL,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__24_validate_user() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_oauthlib$oauth2$rfc6749$request_validator$$$function__24_validate_user,
        mod_consts[88],
#if PYTHON_VERSION >= 0x300
        mod_consts[89],
#endif
        codeobj_99168fe18391008f5fa4fc4155dd7815,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[22],
        NULL,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__25_is_pkce_required() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        NULL,
        mod_consts[91],
#if PYTHON_VERSION >= 0x300
        mod_consts[92],
#endif
        codeobj_67cb4221245cb811c4d7b534a6497083,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[90],
        NULL,
        0
    );
    Nuitka_Function_EnableConstReturnFalse(result);

    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__26_get_code_challenge() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        NULL,
        mod_consts[94],
#if PYTHON_VERSION >= 0x300
        mod_consts[95],
#endif
        codeobj_15868616fd3d30e52f339280b08667d6,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[93],
        NULL,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__27_get_code_challenge_method() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_oauthlib$oauth2$rfc6749$request_validator$$$function__27_get_code_challenge_method,
        mod_consts[96],
#if PYTHON_VERSION >= 0x300
        mod_consts[97],
#endif
        codeobj_ba068dbaf8b68cb9c006b9ee06af5e58,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[23],
        NULL,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__28_is_origin_allowed() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        NULL,
        mod_consts[99],
#if PYTHON_VERSION >= 0x300
        mod_consts[100],
#endif
        codeobj_fca600ed8fd6b12437c84c1597335333,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[98],
        NULL,
        0
    );
    Nuitka_Function_EnableConstReturnFalse(result);

    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__2_authenticate_client() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_oauthlib$oauth2$rfc6749$request_validator$$$function__2_authenticate_client,
        mod_consts[43],
#if PYTHON_VERSION >= 0x300
        mod_consts[44],
#endif
        codeobj_cb20c4dfbed080a14a85811f41839e22,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[1],
        NULL,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__3_authenticate_client_id() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_oauthlib$oauth2$rfc6749$request_validator$$$function__3_authenticate_client_id,
        mod_consts[45],
#if PYTHON_VERSION >= 0x300
        mod_consts[46],
#endif
        codeobj_176cec46e6b5ee76aee1ea4e54060d30,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[2],
        NULL,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__4_confirm_redirect_uri() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_oauthlib$oauth2$rfc6749$request_validator$$$function__4_confirm_redirect_uri,
        mod_consts[47],
#if PYTHON_VERSION >= 0x300
        mod_consts[48],
#endif
        codeobj_2a16f0793529ed9c7bae140e1ea16ad2,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[3],
        NULL,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__5_get_default_redirect_uri() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_oauthlib$oauth2$rfc6749$request_validator$$$function__5_get_default_redirect_uri,
        mod_consts[49],
#if PYTHON_VERSION >= 0x300
        mod_consts[50],
#endif
        codeobj_dfb0755ba293c104853cc61335c50977,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[4],
        NULL,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__6_get_default_scopes() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_oauthlib$oauth2$rfc6749$request_validator$$$function__6_get_default_scopes,
        mod_consts[51],
#if PYTHON_VERSION >= 0x300
        mod_consts[52],
#endif
        codeobj_41a3ece1a35709f73a6c917b7c80bf46,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[5],
        NULL,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__7_get_original_scopes() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_oauthlib$oauth2$rfc6749$request_validator$$$function__7_get_original_scopes,
        mod_consts[53],
#if PYTHON_VERSION >= 0x300
        mod_consts[54],
#endif
        codeobj_17f5e2b7f4eac3a3190f4cbbed334286,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[6],
        NULL,
        0
    );


    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__8_is_within_original_scope() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        NULL,
        mod_consts[56],
#if PYTHON_VERSION >= 0x300
        mod_consts[57],
#endif
        codeobj_590a91faa164b246a361eec1a702b5e4,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[55],
        NULL,
        0
    );
    Nuitka_Function_EnableConstReturnFalse(result);

    return (PyObject *)result;
}



static PyObject *MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__9_introspect_token() {
    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        impl_oauthlib$oauth2$rfc6749$request_validator$$$function__9_introspect_token,
        mod_consts[58],
#if PYTHON_VERSION >= 0x300
        mod_consts[59],
#endif
        codeobj_f2c4f529262545335009559750e8e70e,
        NULL,
#if PYTHON_VERSION >= 0x300
        NULL,
        NULL,
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        mod_consts[7],
        NULL,
        0
    );


    return (PyObject *)result;
}


extern void _initCompiledCellType();
extern void _initCompiledGeneratorType();
extern void _initCompiledFunctionType();
extern void _initCompiledMethodType();
extern void _initCompiledFrameType();

extern PyTypeObject Nuitka_Loader_Type;

#ifdef _NUITKA_PLUGIN_DILL_ENABLED
// Provide a way to create find a function via its C code and create it back
// in another process, useful for multiprocessing extensions like dill
extern void registerDillPluginTables(char const *module_name, PyMethodDef *reduce_compiled_function, PyMethodDef *create_compiled_function);

function_impl_code functable_oauthlib$oauth2$rfc6749$request_validator[] = {
    NULL,
    impl_oauthlib$oauth2$rfc6749$request_validator$$$function__2_authenticate_client,
    impl_oauthlib$oauth2$rfc6749$request_validator$$$function__3_authenticate_client_id,
    impl_oauthlib$oauth2$rfc6749$request_validator$$$function__4_confirm_redirect_uri,
    impl_oauthlib$oauth2$rfc6749$request_validator$$$function__5_get_default_redirect_uri,
    impl_oauthlib$oauth2$rfc6749$request_validator$$$function__6_get_default_scopes,
    impl_oauthlib$oauth2$rfc6749$request_validator$$$function__7_get_original_scopes,
    NULL,
    impl_oauthlib$oauth2$rfc6749$request_validator$$$function__9_introspect_token,
    impl_oauthlib$oauth2$rfc6749$request_validator$$$function__10_invalidate_authorization_code,
    impl_oauthlib$oauth2$rfc6749$request_validator$$$function__11_revoke_token,
    NULL,
    impl_oauthlib$oauth2$rfc6749$request_validator$$$function__13_save_authorization_code,
    impl_oauthlib$oauth2$rfc6749$request_validator$$$function__14_save_token,
    impl_oauthlib$oauth2$rfc6749$request_validator$$$function__15_save_bearer_token,
    impl_oauthlib$oauth2$rfc6749$request_validator$$$function__16_validate_bearer_token,
    impl_oauthlib$oauth2$rfc6749$request_validator$$$function__17_validate_client_id,
    impl_oauthlib$oauth2$rfc6749$request_validator$$$function__18_validate_code,
    impl_oauthlib$oauth2$rfc6749$request_validator$$$function__19_validate_grant_type,
    impl_oauthlib$oauth2$rfc6749$request_validator$$$function__20_validate_redirect_uri,
    impl_oauthlib$oauth2$rfc6749$request_validator$$$function__21_validate_refresh_token,
    impl_oauthlib$oauth2$rfc6749$request_validator$$$function__22_validate_response_type,
    impl_oauthlib$oauth2$rfc6749$request_validator$$$function__23_validate_scopes,
    impl_oauthlib$oauth2$rfc6749$request_validator$$$function__24_validate_user,
    NULL,
    NULL,
    impl_oauthlib$oauth2$rfc6749$request_validator$$$function__27_get_code_challenge_method,
    NULL,
    NULL
};

static char const *_reduce_compiled_function_argnames[] = {
    "func",
    NULL
};

static PyObject *_reduce_compiled_function(PyObject *self, PyObject *args, PyObject *kwds) {
    PyObject *func;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O:reduce_compiled_function", (char **)_reduce_compiled_function_argnames, &func, NULL)) {
        return NULL;
    }

    if (Nuitka_Function_Check(func) == false) {
        SET_CURRENT_EXCEPTION_TYPE0_STR(PyExc_TypeError, "not a compiled function");
        return NULL;
    }

    struct Nuitka_FunctionObject *function = (struct Nuitka_FunctionObject *)func;

    function_impl_code *current = functable_oauthlib$oauth2$rfc6749$request_validator;
    int offset = 0;

    while (*current != NULL) {
        if (*current == function->m_c_code) {
            break;
        }

        current += 1;
        offset += 1;
    }

    if (*current == NULL) {
        SET_CURRENT_EXCEPTION_TYPE0_STR(PyExc_TypeError, "Cannot find compiled function in module.");
        return NULL;
    }

    PyObject *code_object_desc = MAKE_TUPLE_EMPTY(6);
    PyTuple_SET_ITEM0(code_object_desc, 0, function->m_code_object->co_filename);
    PyTuple_SET_ITEM0(code_object_desc, 1, function->m_code_object->co_name);
    PyTuple_SET_ITEM(code_object_desc, 2, PyLong_FromLong(function->m_code_object->co_firstlineno));
    PyTuple_SET_ITEM0(code_object_desc, 3, function->m_code_object->co_varnames);
    PyTuple_SET_ITEM(code_object_desc, 4, PyLong_FromLong(function->m_code_object->co_argcount));
    PyTuple_SET_ITEM(code_object_desc, 5, PyLong_FromLong(function->m_code_object->co_flags));

    CHECK_OBJECT_DEEP(code_object_desc);

    PyObject *result = MAKE_TUPLE_EMPTY(4);
    PyTuple_SET_ITEM(result, 0, PyLong_FromLong(offset));
    PyTuple_SET_ITEM(result, 1, code_object_desc);
    PyTuple_SET_ITEM0(result, 2, function->m_defaults);
    PyTuple_SET_ITEM0(result, 3, function->m_doc != NULL ? function->m_doc : Py_None);

    CHECK_OBJECT_DEEP(result);

    return result;
}

static PyMethodDef _method_def_reduce_compiled_function = {"reduce_compiled_function", (PyCFunction)_reduce_compiled_function,
                                                           METH_VARARGS | METH_KEYWORDS, NULL};

static char const *_create_compiled_function_argnames[] = {
    "func",
    "code_object_desc",
    "defaults",
    "doc",
    NULL
};


static PyObject *_create_compiled_function(PyObject *self, PyObject *args, PyObject *kwds) {
    CHECK_OBJECT_DEEP(args);

    PyObject *func;
    PyObject *code_object_desc;
    PyObject *defaults;
    PyObject *doc;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "OOOO:create_compiled_function", (char **)_create_compiled_function_argnames, &func, &code_object_desc, &defaults, &doc, NULL)) {
        return NULL;
    }

    int offset = PyLong_AsLong(func);

    if (offset == -1 && ERROR_OCCURRED()) {
        return NULL;
    }

    if (offset > sizeof(functable_oauthlib$oauth2$rfc6749$request_validator) || offset < 0) {
        SET_CURRENT_EXCEPTION_TYPE0_STR(PyExc_TypeError, "Wrong offset for compiled function.");
        return NULL;
    }

    PyObject *filename = PyTuple_GET_ITEM(code_object_desc, 0);
    PyObject *function_name = PyTuple_GET_ITEM(code_object_desc, 1);
    PyObject *line = PyTuple_GET_ITEM(code_object_desc, 2);
    int line_int = PyLong_AsLong(line);
    assert(!ERROR_OCCURRED());

    PyObject *argnames = PyTuple_GET_ITEM(code_object_desc, 3);
    PyObject *arg_count = PyTuple_GET_ITEM(code_object_desc, 4);
    int arg_count_int = PyLong_AsLong(arg_count);
    assert(!ERROR_OCCURRED());
    PyObject *flags = PyTuple_GET_ITEM(code_object_desc, 5);
    int flags_int = PyLong_AsLong(flags);
    assert(!ERROR_OCCURRED());

    PyCodeObject *code_object = MAKE_CODE_OBJECT(
        filename,
        line_int,
        flags_int,
        function_name,
        argnames,
        NULL, // freevars
        arg_count_int,
        0, // TODO: Missing kw_only_count
        0 // TODO: Missing pos_only_count
    );

    struct Nuitka_FunctionObject *result = Nuitka_Function_New(
        functable_oauthlib$oauth2$rfc6749$request_validator[offset],
        code_object->co_name,
#if PYTHON_VERSION >= 0x300
        NULL, // TODO: Not transferring qualname yet
#endif
        code_object,
        defaults,
#if PYTHON_VERSION >= 0x300
        NULL, // kwdefaults are done on the outside currently
        NULL, // TODO: Not transferring annotations
#endif
        module_oauthlib$oauth2$rfc6749$request_validator,
        doc,
        NULL,
        0
    );

    return (PyObject *)result;
}

static PyMethodDef _method_def_create_compiled_function = {
    "create_compiled_function",
    (PyCFunction)_create_compiled_function,
    METH_VARARGS | METH_KEYWORDS, NULL
};


#endif

// Internal entry point for module code.
PyObject *modulecode_oauthlib$oauth2$rfc6749$request_validator(PyObject *module, struct Nuitka_MetaPathBasedLoaderEntry const *loader_entry) {
    // Report entry to PGO.
    PGO_onModuleEntered("oauthlib.oauth2.rfc6749.request_validator");

    // Store the module for future use.
    module_oauthlib$oauth2$rfc6749$request_validator = module;

    // Modules can be loaded again in case of errors, avoid the init being done again.
    static bool init_done = false;

    if (init_done == false) {
#if defined(_NUITKA_MODULE) && 0
        // In case of an extension module loaded into a process, we need to call
        // initialization here because that's the first and potentially only time
        // we are going called.

        // Initialize the constant values used.
        _initBuiltinModule();
        createGlobalConstants();

        /* Initialize the compiled types of Nuitka. */
        _initCompiledCellType();
        _initCompiledGeneratorType();
        _initCompiledFunctionType();
        _initCompiledMethodType();
        _initCompiledFrameType();

        _initSlotCompare();
#if PYTHON_VERSION >= 0x270
        _initSlotIterNext();
#endif

        patchTypeComparison();

        // Enable meta path based loader if not already done.
#ifdef _NUITKA_TRACE
        PRINT_STRING("oauthlib.oauth2.rfc6749.request_validator: Calling setupMetaPathBasedLoader().\n");
#endif
        setupMetaPathBasedLoader();

#if PYTHON_VERSION >= 0x300
        patchInspectModule();
#endif

#endif

        /* The constants only used by this module are created now. */
#ifdef _NUITKA_TRACE
        PRINT_STRING("oauthlib.oauth2.rfc6749.request_validator: Calling createModuleConstants().\n");
#endif
        createModuleConstants();

        /* The code objects used by this module are created now. */
#ifdef _NUITKA_TRACE
        PRINT_STRING("oauthlib.oauth2.rfc6749.request_validator: Calling createModuleCodeObjects().\n");
#endif
        createModuleCodeObjects();

        init_done = true;
    }

    // PRINT_STRING("in initoauthlib$oauth2$rfc6749$request_validator\n");

    moduledict_oauthlib$oauth2$rfc6749$request_validator = MODULE_DICT(module_oauthlib$oauth2$rfc6749$request_validator);

#ifdef _NUITKA_PLUGIN_DILL_ENABLED
    registerDillPluginTables(loader_entry->name, &_method_def_reduce_compiled_function, &_method_def_create_compiled_function);
#endif

    // Set "__compiled__" to what version information we have.
    UPDATE_STRING_DICT0(
        moduledict_oauthlib$oauth2$rfc6749$request_validator,
        (Nuitka_StringObject *)const_str_plain___compiled__,
        Nuitka_dunder_compiled_value
    );

    // Update "__package__" value to what it ought to be.
    {
#if 0
        UPDATE_STRING_DICT0(
            moduledict_oauthlib$oauth2$rfc6749$request_validator,
            (Nuitka_StringObject *)const_str_plain___package__,
            mod_consts[124]
        );
#elif 0
        PyObject *module_name = GET_STRING_DICT_VALUE(moduledict_oauthlib$oauth2$rfc6749$request_validator, (Nuitka_StringObject *)const_str_plain___name__);

        UPDATE_STRING_DICT0(
            moduledict_oauthlib$oauth2$rfc6749$request_validator,
            (Nuitka_StringObject *)const_str_plain___package__,
            module_name
        );
#else

#if PYTHON_VERSION < 0x300
        PyObject *module_name = GET_STRING_DICT_VALUE(moduledict_oauthlib$oauth2$rfc6749$request_validator, (Nuitka_StringObject *)const_str_plain___name__);
        char const *module_name_cstr = PyString_AS_STRING(module_name);

        char const *last_dot = strrchr(module_name_cstr, '.');

        if (last_dot != NULL) {
            UPDATE_STRING_DICT1(
                moduledict_oauthlib$oauth2$rfc6749$request_validator,
                (Nuitka_StringObject *)const_str_plain___package__,
                PyString_FromStringAndSize(module_name_cstr, last_dot - module_name_cstr)
            );
        }
#else
        PyObject *module_name = GET_STRING_DICT_VALUE(moduledict_oauthlib$oauth2$rfc6749$request_validator, (Nuitka_StringObject *)const_str_plain___name__);
        Py_ssize_t dot_index = PyUnicode_Find(module_name, const_str_dot, 0, PyUnicode_GetLength(module_name), -1);

        if (dot_index != -1) {
            UPDATE_STRING_DICT1(
                moduledict_oauthlib$oauth2$rfc6749$request_validator,
                (Nuitka_StringObject *)const_str_plain___package__,
                PyUnicode_Substring(module_name, 0, dot_index)
            );
        }
#endif
#endif
    }

    CHECK_OBJECT(module_oauthlib$oauth2$rfc6749$request_validator);

    // For deep importing of a module we need to have "__builtins__", so we set
    // it ourselves in the same way than CPython does. Note: This must be done
    // before the frame object is allocated, or else it may fail.

    if (GET_STRING_DICT_VALUE(moduledict_oauthlib$oauth2$rfc6749$request_validator, (Nuitka_StringObject *)const_str_plain___builtins__) == NULL) {
        PyObject *value = (PyObject *)builtin_module;

        // Check if main module, not a dict then but the module itself.
#if defined(_NUITKA_MODULE) || !0
        value = PyModule_GetDict(value);
#endif

        UPDATE_STRING_DICT0(moduledict_oauthlib$oauth2$rfc6749$request_validator, (Nuitka_StringObject *)const_str_plain___builtins__, value);
    }

    UPDATE_STRING_DICT0(moduledict_oauthlib$oauth2$rfc6749$request_validator, (Nuitka_StringObject *)const_str_plain___loader__, (PyObject *)&Nuitka_Loader_Type);

#if PYTHON_VERSION >= 0x340
// Set the "__spec__" value

#if 0
    // Main modules just get "None" as spec.
    UPDATE_STRING_DICT0(moduledict_oauthlib$oauth2$rfc6749$request_validator, (Nuitka_StringObject *)const_str_plain___spec__, Py_None);
#else
    // Other modules get a "ModuleSpec" from the standard mechanism.
    {
        PyObject *bootstrap_module = getImportLibBootstrapModule();
        CHECK_OBJECT(bootstrap_module);

        PyObject *_spec_from_module = PyObject_GetAttrString(bootstrap_module, "_spec_from_module");
        CHECK_OBJECT(_spec_from_module);

        PyObject *spec_value = CALL_FUNCTION_WITH_SINGLE_ARG(_spec_from_module, module_oauthlib$oauth2$rfc6749$request_validator);
        Py_DECREF(_spec_from_module);

        // We can assume this to never fail, or else we are in trouble anyway.
        // CHECK_OBJECT(spec_value);

        if (spec_value == NULL) {
            PyErr_PrintEx(0);
            abort();
        }

// Mark the execution in the "__spec__" value.
        SET_ATTRIBUTE(spec_value, const_str_plain__initializing, Py_True);

        UPDATE_STRING_DICT1(moduledict_oauthlib$oauth2$rfc6749$request_validator, (Nuitka_StringObject *)const_str_plain___spec__, spec_value);
    }
#endif
#endif

    // Temp variables if any
    PyObject *outline_0_var___class__ = NULL;
    PyObject *tmp_class_creation_1__class_decl_dict = NULL;
    PyObject *tmp_class_creation_1__prepared = NULL;
    struct Nuitka_FrameObject *frame_798142724311027663b78add05f0a5d9;
    NUITKA_MAY_BE_UNUSED char const *type_description_1 = NULL;
    bool tmp_result;
    PyObject *exception_type = NULL;
    PyObject *exception_value = NULL;
    PyTracebackObject *exception_tb = NULL;
    NUITKA_MAY_BE_UNUSED int exception_lineno = 0;
    PyObject *locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10 = NULL;
    PyObject *tmp_dictset_value;
    int tmp_res;
    PyObject *exception_keeper_type_1;
    PyObject *exception_keeper_value_1;
    PyTracebackObject *exception_keeper_tb_1;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_1;
    PyObject *exception_keeper_type_2;
    PyObject *exception_keeper_value_2;
    PyTracebackObject *exception_keeper_tb_2;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_2;
    PyObject *exception_keeper_type_3;
    PyObject *exception_keeper_value_3;
    PyTracebackObject *exception_keeper_tb_3;
    NUITKA_MAY_BE_UNUSED int exception_keeper_lineno_3;

    // Module code.
    {
        PyObject *tmp_assign_source_1;
        tmp_assign_source_1 = mod_consts[24];
        UPDATE_STRING_DICT0(moduledict_oauthlib$oauth2$rfc6749$request_validator, (Nuitka_StringObject *)mod_consts[25], tmp_assign_source_1);
    }
    {
        PyObject *tmp_assign_source_2;
        tmp_assign_source_2 = module_filename_obj;
        UPDATE_STRING_DICT0(moduledict_oauthlib$oauth2$rfc6749$request_validator, (Nuitka_StringObject *)mod_consts[26], tmp_assign_source_2);
    }
    frame_798142724311027663b78add05f0a5d9 = MAKE_MODULE_FRAME(codeobj_798142724311027663b78add05f0a5d9, module_oauthlib$oauth2$rfc6749$request_validator);

    // Push the new frame as the currently active one, and we should be exclusively
    // owning it.
    pushFrameStackCompiledFrame(frame_798142724311027663b78add05f0a5d9);
    assert(Py_REFCNT(frame_798142724311027663b78add05f0a5d9) == 2);

    // Framed code:
    {
        PyObject *tmp_assattr_value_1;
        PyObject *tmp_assattr_target_1;
        tmp_assattr_value_1 = module_filename_obj;
        tmp_assattr_target_1 = GET_STRING_DICT_VALUE(moduledict_oauthlib$oauth2$rfc6749$request_validator, (Nuitka_StringObject *)mod_consts[27]);

        if (unlikely(tmp_assattr_target_1 == NULL)) {
            tmp_assattr_target_1 = GET_MODULE_VARIABLE_VALUE_FALLBACK(mod_consts[27]);
        }

        assert(!(tmp_assattr_target_1 == NULL));
        tmp_result = SET_ATTRIBUTE(tmp_assattr_target_1, mod_consts[28], tmp_assattr_value_1);
        if (tmp_result == false) {
            assert(ERROR_OCCURRED());

            FETCH_ERROR_OCCURRED(&exception_type, &exception_value, &exception_tb);


            exception_lineno = 1;

            goto frame_exception_exit_1;
        }
    }
    {
        PyObject *tmp_assattr_value_2;
        PyObject *tmp_assattr_target_2;
        tmp_assattr_value_2 = Py_True;
        tmp_assattr_target_2 = GET_STRING_DICT_VALUE(moduledict_oauthlib$oauth2$rfc6749$request_validator, (Nuitka_StringObject *)mod_consts[27]);

        if (unlikely(tmp_assattr_target_2 == NULL)) {
            tmp_assattr_target_2 = GET_MODULE_VARIABLE_VALUE_FALLBACK(mod_consts[27]);
        }

        assert(!(tmp_assattr_target_2 == NULL));
        tmp_result = SET_ATTRIBUTE(tmp_assattr_target_2, mod_consts[29], tmp_assattr_value_2);
        if (tmp_result == false) {
            assert(ERROR_OCCURRED());

            FETCH_ERROR_OCCURRED(&exception_type, &exception_value, &exception_tb);


            exception_lineno = 1;

            goto frame_exception_exit_1;
        }
    }
    {
        PyObject *tmp_assign_source_3;
        tmp_assign_source_3 = Py_None;
        UPDATE_STRING_DICT0(moduledict_oauthlib$oauth2$rfc6749$request_validator, (Nuitka_StringObject *)mod_consts[30], tmp_assign_source_3);
    }
    {
        PyObject *tmp_assign_source_4;
        PyObject *tmp_name_value_1;
        PyObject *tmp_globals_arg_value_1;
        PyObject *tmp_locals_arg_value_1;
        PyObject *tmp_fromlist_value_1;
        PyObject *tmp_level_value_1;
        tmp_name_value_1 = mod_consts[31];
        tmp_globals_arg_value_1 = (PyObject *)moduledict_oauthlib$oauth2$rfc6749$request_validator;
        tmp_locals_arg_value_1 = Py_None;
        tmp_fromlist_value_1 = Py_None;
        tmp_level_value_1 = mod_consts[32];
        frame_798142724311027663b78add05f0a5d9->m_frame.f_lineno = 5;
        tmp_assign_source_4 = IMPORT_MODULE5(tmp_name_value_1, tmp_globals_arg_value_1, tmp_locals_arg_value_1, tmp_fromlist_value_1, tmp_level_value_1);
        if (tmp_assign_source_4 == NULL) {
            assert(ERROR_OCCURRED());

            FETCH_ERROR_OCCURRED(&exception_type, &exception_value, &exception_tb);


            exception_lineno = 5;

            goto frame_exception_exit_1;
        }
        UPDATE_STRING_DICT1(moduledict_oauthlib$oauth2$rfc6749$request_validator, (Nuitka_StringObject *)mod_consts[31], tmp_assign_source_4);
    }
    {
        PyObject *tmp_assign_source_5;
        PyObject *tmp_called_instance_1;
        tmp_called_instance_1 = GET_STRING_DICT_VALUE(moduledict_oauthlib$oauth2$rfc6749$request_validator, (Nuitka_StringObject *)mod_consts[31]);

        if (unlikely(tmp_called_instance_1 == NULL)) {
            tmp_called_instance_1 = GET_MODULE_VARIABLE_VALUE_FALLBACK(mod_consts[31]);
        }

        assert(!(tmp_called_instance_1 == NULL));
        frame_798142724311027663b78add05f0a5d9->m_frame.f_lineno = 7;
        tmp_assign_source_5 = CALL_METHOD_WITH_SINGLE_ARG(
            tmp_called_instance_1,
            mod_consts[33],
            PyTuple_GET_ITEM(mod_consts[34], 0)
        );

        if (tmp_assign_source_5 == NULL) {
            assert(ERROR_OCCURRED());

            FETCH_ERROR_OCCURRED(&exception_type, &exception_value, &exception_tb);


            exception_lineno = 7;

            goto frame_exception_exit_1;
        }
        UPDATE_STRING_DICT1(moduledict_oauthlib$oauth2$rfc6749$request_validator, (Nuitka_StringObject *)mod_consts[35], tmp_assign_source_5);
    }
    {
        PyObject *tmp_assign_source_6;
        tmp_assign_source_6 = MAKE_DICT_EMPTY();
        assert(tmp_class_creation_1__class_decl_dict == NULL);
        tmp_class_creation_1__class_decl_dict = tmp_assign_source_6;
    }
    {
        PyObject *tmp_assign_source_7;
        tmp_assign_source_7 = MAKE_DICT_EMPTY();
        assert(tmp_class_creation_1__prepared == NULL);
        tmp_class_creation_1__prepared = tmp_assign_source_7;
    }
    // Tried code:
    {
        PyObject *tmp_assign_source_8;
        {
            PyObject *tmp_set_locals_1;
            CHECK_OBJECT(tmp_class_creation_1__prepared);
            tmp_set_locals_1 = tmp_class_creation_1__prepared;
            locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10 = tmp_set_locals_1;
            Py_INCREF(tmp_set_locals_1);
        }
        tmp_dictset_value = mod_consts[36];
        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[37], tmp_dictset_value);
        assert(!(tmp_res != 0));
        tmp_dictset_value = mod_consts[38];
        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[39], tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__1_client_authentication_required();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[41], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__2_authenticate_client();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[43], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__3_authenticate_client_id();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[45], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__4_confirm_redirect_uri();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[47], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__5_get_default_redirect_uri();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[49], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__6_get_default_scopes();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[51], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__7_get_original_scopes();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[53], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__8_is_within_original_scope();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[56], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__9_introspect_token();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[58], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__10_invalidate_authorization_code();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[60], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__11_revoke_token();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[62], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__12_rotate_refresh_token();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[65], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__13_save_authorization_code();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[67], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__14_save_token();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[69], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__15_save_bearer_token();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[11], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__16_validate_bearer_token();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[72], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__17_validate_client_id();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[74], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__18_validate_code();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[76], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__19_validate_grant_type();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[78], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__20_validate_redirect_uri();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[80], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__21_validate_refresh_token();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[82], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__22_validate_response_type();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[84], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__23_validate_scopes();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[86], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__24_validate_user();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[88], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__25_is_pkce_required();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[91], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__26_get_code_challenge();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[94], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__27_get_code_challenge_method();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[96], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));


        tmp_dictset_value = MAKE_FUNCTION_oauthlib$oauth2$rfc6749$request_validator$$$function__28_is_origin_allowed();

        tmp_res = PyDict_SetItem(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10, mod_consts[99], tmp_dictset_value);
        Py_DECREF(tmp_dictset_value);
        assert(!(tmp_res != 0));
        // Tried code:
        // Tried code:
        {
            PyObject *tmp_assign_source_9;
            PyObject *tmp_called_value_1;
            PyObject *tmp_args_value_1;
            PyObject *tmp_tuple_element_1;
            PyObject *tmp_kwargs_value_1;
            tmp_called_value_1 = (PyObject *)&PyType_Type;
            tmp_tuple_element_1 = mod_consts[38];
            tmp_args_value_1 = MAKE_TUPLE_EMPTY(3);
            PyTuple_SET_ITEM0(tmp_args_value_1, 0, tmp_tuple_element_1);
            tmp_tuple_element_1 = mod_consts[101];
            PyTuple_SET_ITEM0(tmp_args_value_1, 1, tmp_tuple_element_1);
            tmp_tuple_element_1 = locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10;
            PyTuple_SET_ITEM0(tmp_args_value_1, 2, tmp_tuple_element_1);
            CHECK_OBJECT(tmp_class_creation_1__class_decl_dict);
            tmp_kwargs_value_1 = tmp_class_creation_1__class_decl_dict;
            frame_798142724311027663b78add05f0a5d9->m_frame.f_lineno = 10;
            tmp_assign_source_9 = CALL_FUNCTION(tmp_called_value_1, tmp_args_value_1, tmp_kwargs_value_1);
            Py_DECREF(tmp_args_value_1);
            if (tmp_assign_source_9 == NULL) {
                assert(ERROR_OCCURRED());

                FETCH_ERROR_OCCURRED(&exception_type, &exception_value, &exception_tb);


                exception_lineno = 10;

                goto try_except_handler_3;
            }
            assert(outline_0_var___class__ == NULL);
            outline_0_var___class__ = tmp_assign_source_9;
        }
        CHECK_OBJECT(outline_0_var___class__);
        tmp_assign_source_8 = outline_0_var___class__;
        Py_INCREF(tmp_assign_source_8);
        goto try_return_handler_3;
        NUITKA_CANNOT_GET_HERE("tried codes exits in all cases");
        return NULL;
        // Return handler code:
        try_return_handler_3:;
        Py_DECREF(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10);
        locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10 = NULL;
        goto try_return_handler_2;
        // Exception handler code:
        try_except_handler_3:;
        exception_keeper_type_1 = exception_type;
        exception_keeper_value_1 = exception_value;
        exception_keeper_tb_1 = exception_tb;
        exception_keeper_lineno_1 = exception_lineno;
        exception_type = NULL;
        exception_value = NULL;
        exception_tb = NULL;
        exception_lineno = 0;

        Py_DECREF(locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10);
        locals_oauthlib$oauth2$rfc6749$request_validator$$$class__1_RequestValidator_10 = NULL;
        // Re-raise.
        exception_type = exception_keeper_type_1;
        exception_value = exception_keeper_value_1;
        exception_tb = exception_keeper_tb_1;
        exception_lineno = exception_keeper_lineno_1;

        goto try_except_handler_2;
        // End of try:
        NUITKA_CANNOT_GET_HERE("tried codes exits in all cases");
        return NULL;
        // Return handler code:
        try_return_handler_2:;
        CHECK_OBJECT(outline_0_var___class__);
        Py_DECREF(outline_0_var___class__);
        outline_0_var___class__ = NULL;
        goto outline_result_1;
        // Exception handler code:
        try_except_handler_2:;
        exception_keeper_type_2 = exception_type;
        exception_keeper_value_2 = exception_value;
        exception_keeper_tb_2 = exception_tb;
        exception_keeper_lineno_2 = exception_lineno;
        exception_type = NULL;
        exception_value = NULL;
        exception_tb = NULL;
        exception_lineno = 0;

        // Re-raise.
        exception_type = exception_keeper_type_2;
        exception_value = exception_keeper_value_2;
        exception_tb = exception_keeper_tb_2;
        exception_lineno = exception_keeper_lineno_2;

        goto outline_exception_1;
        // End of try:
        NUITKA_CANNOT_GET_HERE("Return statement must have exited already.");
        return NULL;
        outline_exception_1:;
        exception_lineno = 10;
        goto try_except_handler_1;
        outline_result_1:;
        UPDATE_STRING_DICT1(moduledict_oauthlib$oauth2$rfc6749$request_validator, (Nuitka_StringObject *)mod_consts[38], tmp_assign_source_8);
    }
    goto try_end_1;
    // Exception handler code:
    try_except_handler_1:;
    exception_keeper_type_3 = exception_type;
    exception_keeper_value_3 = exception_value;
    exception_keeper_tb_3 = exception_tb;
    exception_keeper_lineno_3 = exception_lineno;
    exception_type = NULL;
    exception_value = NULL;
    exception_tb = NULL;
    exception_lineno = 0;

    CHECK_OBJECT(tmp_class_creation_1__class_decl_dict);
    Py_DECREF(tmp_class_creation_1__class_decl_dict);
    tmp_class_creation_1__class_decl_dict = NULL;
    CHECK_OBJECT(tmp_class_creation_1__prepared);
    Py_DECREF(tmp_class_creation_1__prepared);
    tmp_class_creation_1__prepared = NULL;
    // Re-raise.
    exception_type = exception_keeper_type_3;
    exception_value = exception_keeper_value_3;
    exception_tb = exception_keeper_tb_3;
    exception_lineno = exception_keeper_lineno_3;

    goto frame_exception_exit_1;
    // End of try:
    try_end_1:;


    // Put the previous frame back on top.
    popFrameStack();

    goto frame_no_exception_1;
    frame_exception_exit_1:


    if (exception_tb == NULL) {
        exception_tb = MAKE_TRACEBACK(frame_798142724311027663b78add05f0a5d9, exception_lineno);
    } else if (exception_tb->tb_frame != &frame_798142724311027663b78add05f0a5d9->m_frame) {
        exception_tb = ADD_TRACEBACK(exception_tb, frame_798142724311027663b78add05f0a5d9, exception_lineno);
    }



    assertFrameObject(frame_798142724311027663b78add05f0a5d9);

    // Put the previous frame back on top.
    popFrameStack();

    // Return the error.
    goto module_exception_exit;
    frame_no_exception_1:;
    CHECK_OBJECT(tmp_class_creation_1__class_decl_dict);
    Py_DECREF(tmp_class_creation_1__class_decl_dict);
    tmp_class_creation_1__class_decl_dict = NULL;
    CHECK_OBJECT(tmp_class_creation_1__prepared);
    Py_DECREF(tmp_class_creation_1__prepared);
    tmp_class_creation_1__prepared = NULL;

    // Report to PGO about leaving the module without error.
    PGO_onModuleExit("oauthlib.oauth2.rfc6749.request_validator", false);

    Py_INCREF(module_oauthlib$oauth2$rfc6749$request_validator);
    return module_oauthlib$oauth2$rfc6749$request_validator;
    module_exception_exit:

#if defined(_NUITKA_MODULE) && 0
    {
        PyObject *module_name = GET_STRING_DICT_VALUE(moduledict_oauthlib$oauth2$rfc6749$request_validator, (Nuitka_StringObject *)const_str_plain___name__);

        if (module_name != NULL) {
            Nuitka_DelModule(module_name);
        }
    }
#endif
    PGO_onModuleExit("oauthlib$oauth2$rfc6749$request_validator", false);

    RESTORE_ERROR_OCCURRED(exception_type, exception_value, exception_tb);
    return NULL;
}
